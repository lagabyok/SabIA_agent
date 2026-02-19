"""
Extrae las 4 historias del pipeline real ejecutado.
H1: Ranking por margen
H2: Tiempo vs margen
H3: Alertas
H4: Drivers de costos
"""

from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)

def extract_story_1_ranking(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    H1: Ranking de productos por margen real
    """
    metrics = output.get("metrics", {})
    productos = metrics.get("productos", [])
    
    # Ordenar por margen
    ranking = sorted(
        productos,
        key=lambda x: x.get("margen_pct", 0),
        reverse=True
    )
    
    bottom_risk = [p for p in ranking if p.get("margen_pct", 0) < 0.1]
    
    return {
        "story_id": 1,
        "title": "Ranking de productos por margen real",
        "subtitle": "¿Qué productos realmente me dejan dinero?",
        "periodo": output.get("periodo", ""),
        "ranking": ranking[:5],
        "bottom_risk": bottom_risk[:3]
    }

def extract_story_2_tiempo_margen(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    H2: Tiempo de producción vs Margen
    """
    metrics = output.get("metrics", {})
    productos = metrics.get("productos", [])
    
    items = []
    for prod in productos:
        item = {
            "servicio_id": prod.get("producto_id", ""),
            "nombre_servicio": prod.get("nombre_producto", ""),
            "minutos_trabajo": prod.get("tiempo_produccion_minutos", 0),
            "margen_pct": prod.get("margen_pct", 0),
            "margen_abs": prod.get("margen_abs_unit", 0) * prod.get("unidades", 0),
            "categoria": "eficiente" if prod.get("margen_pct", 0) > 0.15 else "alto_esfuerzo_bajo_retorno"
        }
        items.append(item)
    
    return {
        "story_id": 2,
        "title": "Tiempo de producción vs Margen",
        "subtitle": "¿Qué productos me quitan mucho tiempo con poco retorno?",
        "empresa": output.get("empresa", "Demo"),
        "thresholds": {
            "esfuerzo_alto_minutos": 300,
            "margen_bajo_pct": 0.15
        },
        "items": items
    }

def extract_story_3_alertas(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    H3: Alertas de rentabilidad
    """
    alerts = output.get("alerts", [])
    
    # Transformar alertas al formato story
    stories_alerts = []
    for alert in alerts[:5]:
        stories_alerts.append({
            "alert_id": alert.get("alert_id", ""),
            "servicio_id": alert.get("producto_id", ""),
            "nombre_servicio": alert.get("nombre_producto", ""),
            "tipo": alert.get("tipo", ""),
            "severidad": alert.get("severidad", "MEDIA"),
            "explicacion_breve": alert.get("explicacion", ""),
            "accion_sugerida": alert.get("accion_sugerida", ""),
            "impacto_estimado": alert.get("evidencia", {})
        })
    
    return {
        "story_id": 3,
        "title": "Alertas de rentabilidad",
        "subtitle": "Productos con problemas que requieren acción",
        "empresa": output.get("empresa", "Demo"),
        "alerts": stories_alerts
    }

def extract_story_4_drivers(output: Dict[str, Any]) -> Dict[str, Any]:
    """
    H4: Drivers de costos
    """
    metrics = output.get("metrics", {})
    recipe_drivers = output.get("recipe_drivers", {})
    
    # Top insumos
    top_insumos = []
    if recipe_drivers:
        insumos_dict = {}
        for prod_id, drivers in recipe_drivers.items():
            if isinstance(drivers, dict):
                for insumo, costo in drivers.items():
                    if insumo not in insumos_dict:
                        insumos_dict[insumo] = 0
                    insumos_dict[insumo] += costo
        
        sorted_insumos = sorted(insumos_dict.items(), key=lambda x: x[1], reverse=True)
        top_insumos = [
            {
                "insumo": insumo,
                "impacto_total": costo,
                "variacion_pct": 0.1  # Simulado
            }
            for insumo, costo in sorted_insumos[:4]
        ]
    
    # Gastos indirectos (si existen en metrics)
    top_gastos_indirectos = metrics.get("gastos_indirectos", [])[:3]
    
    return {
        "story_id": 4,
        "title": "Drivers de costos",
        "subtitle": "¿Dónde enfocar ajustes?",
        "empresa": output.get("empresa", "Demo"),
        "top_insumos": top_insumos,
        "top_gastos_indirectos": top_gastos_indirectos,
        "drivers_por_producto": []
    }
