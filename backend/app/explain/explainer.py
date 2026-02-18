from typing import Dict, Any, List
import pandas as pd

def top_drivers_for_product(recipe_drivers: pd.DataFrame, producto_id: str, top_n: int) -> List[Dict[str, Any]]:
    df = recipe_drivers[recipe_drivers["producto_id"] == producto_id].copy()
    if df.empty:
        return []
    df = df.sort_values("costo_insumo_unit", ascending=False).head(top_n)
    return [
        {"tipo": "INSUMO", "nombre": str(r["nombre_insumo"]), "impacto_unitario": float(r["costo_insumo_unit"])}
        for _, r in df.iterrows()
    ]

def attach_evidence(
    alerts: List[Dict[str, Any]],
    metrics: pd.DataFrame,
    recipe_drivers: pd.DataFrame,
    top_n_drivers: int
) -> List[Dict[str, Any]]:
    m_idx = metrics.set_index("producto_id")

    out = []
    for idx, a in enumerate(alerts, start=1):
        pid = str(a["producto_id"])
        row = m_idx.loc[pid]

        drivers = top_drivers_for_product(recipe_drivers, pid, top_n_drivers)

        evidencia = {
            "precio": float(row["precio"]),
            "costo_total_unit": float(row["costo_total_unit"]),
            "costo_insumos_unit": float(row["costo_insumos_unit"]),
            "costo_esfuerzo_unit": float(row["costo_esfuerzo_unit"]),
            "costo_indirectos_unit": float(row["costo_indirectos_unit"]),
            "margen_abs_unit": float(row["margen_abs_unit"]),
            "margen_pct": float(row["margen_pct"]),
            "unidades_periodo": float(row["unidades_periodo"]),
            "contribucion_total": float(row["contribucion_total"]),
            "perdida_total": float(row["perdida_total"]),
            "tiempo_total_min": float(row["tiempo_total_min"]),
            "drivers": drivers
        }

        # impacto estimado simple: si subo a precio_sugerido, diferencia * unidades
        impacto = {}
        rec = a.get("recomendacion", {})
        ps = rec.get("precio_sugerido")
        if ps is not None and row["unidades_periodo"] > 0:
            impacto["impacto_si_ajusta_precio"] = float((float(ps) - float(row["precio"])) * float(row["unidades_periodo"]))
        if row["perdida_total"] > 0:
            impacto["perdida_actual_periodo"] = float(row["perdida_total"])

        out.append({
            "alert_id": f"A-{idx:04d}",
            **a,
            "evidencia": evidencia,
            "impacto_estimado": impacto
        })
    return out
