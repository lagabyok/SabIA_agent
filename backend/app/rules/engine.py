from typing import List, Dict, Any
import pandas as pd

def build_alerts(
    metrics: pd.DataFrame,
    margen_critico_pct: float,
    margen_objetivo_pct: float,
    esfuerzo_alto_min: int
) -> List[Dict[str, Any]]:
    alerts: List[Dict[str, Any]] = []

    for _, r in metrics.iterrows():
        producto_id = str(r["producto_id"])
        nombre = str(r["nombre_producto"])
        precio = float(r["precio"])
        costo_total = float(r["costo_total_unit"])
        margen_abs = float(r["margen_abs_unit"])
        margen_pct = float(r["margen_pct"]) if r["margen_pct"] is not None else 0.0
        unidades = float(r["unidades_periodo"])
        tiempo = float(r["tiempo_total_min"])

        # Helper precio sugerido
        def precio_sugerido():
            if margen_objetivo_pct >= 1.0:
                return None
            return (costo_total / (1.0 - margen_objetivo_pct)) if (1.0 - margen_objetivo_pct) else None

        # Margen negativo
        if margen_abs < 0:
            alerts.append({
                "producto_id": producto_id,
                "nombre_producto": nombre,
                "tipo": "MARGEN_NEGATIVO",
                "severidad": "ALTA",
                "mensaje": "El costo total por unidad supera el precio de venta.",
                "recomendacion": {
                    "accion": "AJUSTAR_PRECIO",
                    "precio_sugerido": precio_sugerido(),
                    "margen_objetivo_pct": margen_objetivo_pct
                }
            })
            continue

        # Margen crítico
        if 0 <= margen_pct < margen_critico_pct:
            alerts.append({
                "producto_id": producto_id,
                "nombre_producto": nombre,
                "tipo": "MARGEN_CRITICO",
                "severidad": "MEDIA",
                "mensaje": "El margen está por debajo del umbral crítico.",
                "recomendacion": {
                    "accion": "REVISAR_PRECIO_O_COSTOS",
                    "precio_sugerido": precio_sugerido(),
                    "margen_objetivo_pct": margen_objetivo_pct
                }
            })

        # Alto esfuerzo / bajo retorno
        # criterio simple: esfuerzo alto y margen bajo (abs)
        if tiempo >= float(esfuerzo_alto_min) and margen_abs <= (0.5 * precio * margen_critico_pct):
            alerts.append({
                "producto_id": producto_id,
                "nombre_producto": nombre,
                "tipo": "ALTO_ESFUERZO_BAJO_RETORNO",
                "severidad": "MEDIA",
                "mensaje": "Alto tiempo de producción con retorno bajo por unidad.",
                "recomendacion": {
                    "accion": "OPTIMIZAR_O_PRIORIZAR",
                    "nota": "Revisar proceso/receta o priorizar productos con mejor retorno."
                }
            })

        # Precio “desactualizado” (proxy): costo_total muy cerca del precio
        # en demo no tenemos histórico, así que usamos cercanía al precio
        if precio > 0 and (costo_total / precio) >= (1.0 - (margen_critico_pct / 2.0)):
            alerts.append({
                "producto_id": producto_id,
                "nombre_producto": nombre,
                "tipo": "PRECIO_DESACTUALIZADO",
                "severidad": "MEDIA",
                "mensaje": "El costo actual está muy cerca del precio; riesgo de quedar sin margen.",
                "recomendacion": {
                    "accion": "AJUSTAR_PRECIO",
                    "precio_sugerido": precio_sugerido(),
                    "margen_objetivo_pct": margen_objetivo_pct
                }
            })

    return alerts
