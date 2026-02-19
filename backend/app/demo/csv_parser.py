"""
Procesa archivos CSV subidos y genera historias simuladas.
"""

from typing import Dict, Any
import pandas as pd
import logging
from io import BytesIO

logger = logging.getLogger(__name__)

def parse_productos_csv(csv_content: bytes) -> Dict[str, Any]:
    """
    Parsea un CSV de productos y genera H1 (ranking margen)
    Esperado: producto_id, nombre_producto, precio_venta, costo_total_unit, unidades
    """
    try:
        df = pd.read_csv(BytesIO(csv_content))
        
        # Calcular margen si no existe
        if 'margen_pct' not in df.columns:
            df['margen_pct'] = (df['precio_venta'] - df['costo_total_unit']) / df['precio_venta']
        
        if 'margen_abs_unit' not in df.columns:
            df['margen_abs_unit'] = df['precio_venta'] - df['costo_total_unit']
        
        if 'contribucion_total' not in df.columns:
            df['contribucion_total'] = df['margen_abs_unit'] * df['unidades']
        
        # Ordenar por margen
        ranking = df.sort_values('margen_pct', ascending=False).head(5)
        bottom_risk = df[df['margen_pct'] < 0.1].head(3)
        
        return {
            "story_id": 1,
            "title": "Ranking de productos por margen real",
            "subtitle": "¿Qué productos realmente me dejan dinero?",
            "ranking": ranking[['producto_id', 'nombre_producto', 'precio_venta', 'costo_total_unit', 
                               'margen_abs_unit', 'margen_pct', 'unidades', 'contribucion_total']].to_dict('records'),
            "bottom_risk": bottom_risk[['producto_id', 'nombre_producto', 'precio_venta', 'costo_total_unit',
                                       'margen_abs_unit', 'margen_pct', 'unidades', 'contribucion_total']].to_dict('records')
        }
    except Exception as e:
        logger.error(f"Error parseando CSV: {str(e)}")
        return None

def parse_tiempo_csv(csv_content: bytes) -> Dict[str, Any]:
    """
    Parsea un CSV con tiempos y márgenes, genera H2
    Esperado: producto_id, nombre_producto, tiempo_produccion_minutos, margen_pct, margen_abs_unit, unidades
    """
    try:
        df = pd.read_csv(BytesIO(csv_content))
        
        # Categorizar por eficiencia
        def categorizar(row):
            if row.get('margen_pct', 0) > 0.15:
                return 'eficiente'
            else:
                return 'alto_esfuerzo_bajo_retorno'
        
        df['categoria'] = df.apply(categorizar, axis=1)
        df['margen_abs'] = df['margen_abs_unit'] * df['unidades']
        
        items = df[['producto_id', 'nombre_producto', 'tiempo_produccion_minutos', 
                   'margen_pct', 'margen_abs', 'categoria']].to_dict('records')
        
        return {
            "story_id": 2,
            "title": "Tiempo de producción vs Margen",
            "subtitle": "¿Qué productos me quitan mucho tiempo con poco retorno?",
            "thresholds": {
                "esfuerzo_alto_minutos": 300,
                "margen_bajo_pct": 0.15
            },
            "items": items
        }
    except Exception as e:
        logger.error(f"Error parseando CSV tiempos: {str(e)}")
        return None
