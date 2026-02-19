"""
Datos simulados para H1 y H2 según tipo de negocio.
"""

# H1: Panadería - Ranking por margen
PANADERIA_H1 = {
    "story_id": 1,
    "title": "Ranking de productos por margen real",
    "subtitle": "¿Qué productos realmente me dejan dinero?",
    "tipo_negocio": "Panadería",
    "ranking": [
        {
            "nombre_producto": "Muffin vainilla",
            "margen_pct": 0.472,
            "precio_venta": 1800,
            "costo_total_unit": 950,
            "contribucion_total": 102000
        },
        {
            "nombre_producto": "Alfajor",
            "margen_pct": 0.422,
            "precio_venta": 900,
            "costo_total_unit": 520,
            "contribucion_total": 79800
        },
        {
            "nombre_producto": "Torta de chocolate",
            "margen_pct": 0.4,
            "precio_venta": 3500,
            "costo_total_unit": 2100,
            "contribucion_total": 63000
        }
    ],
    "bottom_risk": [
        {
            "nombre_producto": "Galletas con chocolate",
            "margen_pct": -0.208,
            "precio_venta": 1200,
            "costo_total_unit": 1450,
            "perdida_total": -20000
        }
    ]
}

# H2: Panadería - Tiempo vs margen
PANADERIA_H2 = {
    "story_id": 2,
    "title": "Tiempo de producción vs Margen",
    "subtitle": "¿Qué productos me quitan mucho tiempo con poco retorno?",
    "tipo_negocio": "Panadería",
    "items": [
        {
            "nombre_producto": "Muffin vainilla",
            "minutos_trabajo": 45,
            "margen_pct": 0.472,
            "categoria": "eficiente"
        },
        {
            "nombre_producto": "Torta de chocolate",
            "minutos_trabajo": 180,
            "margen_pct": 0.4,
            "categoria": "eficiente"
        },
        {
            "nombre_producto": "Pan integral",
            "minutos_trabajo": 240,
            "margen_pct": 0.025,
            "categoria": "alto_esfuerzo_bajo_retorno"
        },
        {
            "nombre_producto": "Galletas con chocolate",
            "minutos_trabajo": 120,
            "margen_pct": -0.208,
            "categoria": "alto_esfuerzo_bajo_retorno"
        }
    ]
}

# H1: Muebles - Ranking por margen
MUEBLES_H1 = {
    "story_id": 1,
    "title": "Ranking de productos por margen real",
    "subtitle": "¿Qué productos realmente me dejan dinero?",
    "tipo_negocio": "Mueblería",
    "ranking": [
        {
            "nombre_producto": "Mesa comedor 6 personas",
            "margen_pct": 0.45,
            "precio_venta": 85000,
            "costo_total_unit": 46750,
            "contribucion_total": 342000
        },
        {
            "nombre_producto": "Silla de madera",
            "margen_pct": 0.40,
            "precio_venta": 12000,
            "costo_total_unit": 7200,
            "contribucion_total": 180000
        },
        {
            "nombre_producto": "Estantería de roble",
            "margen_pct": 0.38,
            "precio_venta": 45000,
            "costo_total_unit": 27900,
            "contribucion_total": 102600
        }
    ],
    "bottom_risk": [
        {
            "nombre_producto": "Banqueta auxiliar",
            "margen_pct": 0.08,
            "precio_venta": 8000,
            "costo_total_unit": 7360,
            "contribucion_total": 2560
        }
    ]
}

# H2: Muebles - Tiempo vs margen
MUEBLES_H2 = {
    "story_id": 2,
    "title": "Tiempo de producción vs Margen",
    "subtitle": "¿Qué productos me quitan mucho tiempo con poco retorno?",
    "tipo_negocio": "Mueblería",
    "items": [
        {
            "nombre_producto": "Mesa comedor 6 personas",
            "minutos_trabajo": 480,
            "margen_pct": 0.45,
            "categoria": "eficiente"
        },
        {
            "nombre_producto": "Silla de madera",
            "minutos_trabajo": 120,
            "margen_pct": 0.40,
            "categoria": "eficiente"
        },
        {
            "nombre_producto": "Estantería de roble",
            "minutos_trabajo": 360,
            "margen_pct": 0.38,
            "categoria": "eficiente"
        },
        {
            "nombre_producto": "Banqueta auxiliar",
            "minutos_trabajo": 240,
            "margen_pct": 0.08,
            "categoria": "alto_esfuerzo_bajo_retorno"
        }
    ]
}

def get_story_by_filename(filename: str, story_id: int):
    """
    Devuelve H1 o H2 simulada según el nombre del archivo.
    filename: "panaderia_productos.csv" o "mueble_productos.csv"
    story_id: 1 o 2
    """
    filename_lower = filename.lower()
    
    if "panaderia" in filename_lower or "pan" in filename_lower:
        if story_id == 1:
            return PANADERIA_H1
        elif story_id == 2:
            return PANADERIA_H2
    
    elif "mueble" in filename_lower or "furniture" in filename_lower:
        if story_id == 1:
            return MUEBLES_H1
        elif story_id == 2:
            return MUEBLES_H2
    
    # Default: Panadería
    if story_id == 1:
        return PANADERIA_H1
    elif story_id == 2:
        return PANADERIA_H2
    
    return None
