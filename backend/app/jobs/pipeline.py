from typing import Dict, Any, Optional
from datetime import datetime
import pandas as pd
import logging

from app.ingest.loaders import load_csvs
from app.compute.costs import compute_costs
from app.compute.metrics import compute_metrics
from app.rules.engine import build_alerts
from app.explain.explainer import attach_evidence
from app.storage.db import save_run

logger = logging.getLogger(__name__)

def _period_filter(ventas: pd.DataFrame, periodo: str) -> pd.DataFrame:
    # periodo "YYYY-MM" (demo simple)
    # ventas.fecha puede venir como string; lo parseamos
    v = ventas.copy()
    v["fecha"] = pd.to_datetime(v["fecha"], errors="coerce")
    y, m = periodo.split("-")
    y, m = int(y), int(m)
    return v[(v["fecha"].dt.year == y) & (v["fecha"].dt.month == m)].dropna(subset=["fecha"])

def run_all(
    *,
    data_dir: str,
    db_path: str,
    periodo: str,
    valor_minuto: float,
    margen_critico_pct: float,
    margen_objetivo_pct: float,
    esfuerzo_alto_min: int,
    top_drivers: int,
    llm_provider=None
) -> Dict[str, Any]:
    dfs = load_csvs(data_dir)

    # Filtrar ventas por periodo (para que el run sea consistente)
    dfs["ventas"] = _period_filter(dfs["ventas"], periodo)

    unit_costs, recipe_drivers = compute_costs(dfs, valor_minuto=valor_minuto)
    metrics = compute_metrics(dfs, unit_costs=unit_costs)

    alerts = build_alerts(
        metrics,
        margen_critico_pct=margen_critico_pct,
        margen_objetivo_pct=margen_objetivo_pct,
        esfuerzo_alto_min=esfuerzo_alto_min
    )
    alerts = attach_evidence(alerts, metrics, recipe_drivers, top_n_drivers=top_drivers)

    kpis = _kpis_from_metrics(metrics, alerts, periodo)

    payload = {
        "periodo": periodo,
        "kpis": kpis,
        "alerts": alerts
    }

    executive_md = None
    if llm_provider is not None:
        logger.info(f"Llamando al LLM provider: {type(llm_provider).__name__}")
        logger.info(f"Payload contiene {len(alerts)} alertas")
        try:
            executive_md = llm_provider.generate_executive_report(payload)
            logger.info(f"LLM respondió con {len(executive_md) if executive_md else 0} caracteres")
        except Exception as e:
            logger.error(f"Error al llamar al LLM: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
    else:
        logger.info("No se proporcionó LLM provider")

    run_id = datetime.utcnow().isoformat() + "Z"
    output = {
        "run_id": run_id,
        "periodo": periodo,
        "executive_report_md": executive_md or _fallback_report(kpis, alerts),
        "kpis": kpis,
        "alerts": alerts
    }

    save_run(db_path, run_id=run_id, periodo=periodo, output=output)
    return output

def _kpis_from_metrics(metrics: pd.DataFrame, alerts: list, periodo: str) -> Dict[str, Any]:
    total_productos = int(metrics["producto_id"].nunique())

    neg = sum(1 for a in alerts if a["tipo"] == "MARGEN_NEGATIVO")
    crit = sum(1 for a in alerts if a["tipo"] == "MARGEN_CRITICO")
    des = sum(1 for a in alerts if a["tipo"] == "PRECIO_DESACTUALIZADO")
    eff = sum(1 for a in alerts if a["tipo"] == "ALTO_ESFUERZO_BAJO_RETORNO")

    # Margen promedio ponderado por unidades (sobre precio)
    denom = float((metrics["precio"] * metrics["unidades_periodo"]).sum())
    numer = float((metrics["margen_abs_unit"] * metrics["unidades_periodo"]).sum())
    margen_promedio_pct = (numer / denom) if denom else 0.0

    contrib_total = float(metrics["contribucion_total"].sum())
    perdida_total = float(metrics["perdida_total"].sum())

    top_contrib = (
        metrics.sort_values("contribucion_total", ascending=False)
        .head(5)[["producto_id", "nombre_producto", "contribucion_total"]]
        .to_dict(orient="records")
    )
    top_perdida = (
        metrics.sort_values("perdida_total", ascending=False)
        .head(5)[["producto_id", "nombre_producto", "perdida_total"]]
        .to_dict(orient="records")
    )

    return {
        "periodo": periodo,
        "total_productos": total_productos,
        "productos_margen_negativo_count": int(neg),
        "productos_margen_critico_count": int(crit),
        "productos_precio_desactualizado_count": int(des),
        "productos_alto_esfuerzo_bajo_retorno_count": int(eff),
        "margen_promedio_pct": float(margen_promedio_pct),
        "contribucion_total": float(contrib_total),
        "perdida_total_margen_negativo": float(perdida_total),
        "top_5_productos_por_contribucion": top_contrib,
        "top_5_productos_por_perdida": top_perdida,
    }

def _fallback_report(kpis: Dict[str, Any], alerts: list) -> str:
    # Reporte deterministic (sin IA)
    top_alerts = sorted(alerts, key=lambda a: {"ALTA": 0, "MEDIA": 1, "BAJA": 2}.get(a["severidad"], 9))[:3]
    lines = []
    lines.append("### Resumen")
    lines.append(f"- Productos analizados: {kpis['total_productos']}")
    lines.append(f"- Margen negativo: {kpis['productos_margen_negativo_count']} | Margen crítico: {kpis['productos_margen_critico_count']}")
    lines.append(f"- Pérdida estimada por margen negativo: {kpis['perdida_total_margen_negativo']:.2f}")
    lines.append("")
    lines.append("### Alertas clave")
    for a in top_alerts:
        lines.append(f"- **{a['tipo']}** ({a['severidad']}): {a['nombre_producto']} — {a['mensaje']}")
    lines.append("")
    lines.append("### Próximas acciones")
    lines.append("- Ajustar precios sugeridos en productos con margen negativo/crítico.")
    lines.append("- Revisar drivers de costo (insumos dominantes) y tiempos altos.")
    return "\n".join(lines)
