"""
Datos simulados para las 4 historias de demostración.
"""

# HISTORY 1: Ranking por margen real
STORY_1_DATA = {
    "story_id": 1,
    "title": "Ranking de productos por margen real",
    "subtitle": "¿Qué productos realmente me dejan dinero?",
    "periodo": "2026-02",
    "ranking": [
        {
            "producto_id": "P04",
            "nombre_producto": "Muffin vainilla",
            "precio_venta": 1800,
            "costo_total_unit": 950,
            "margen_abs_unit": 850,
            "margen_pct": 0.472,
            "unidades": 120,
            "contribucion_total": 102000
        },
        {
            "producto_id": "P07",
            "nombre_producto": "Alfajor",
            "precio_venta": 900,
            "costo_total_unit": 520,
            "margen_abs_unit": 380,
            "margen_pct": 0.422,
            "unidades": 210,
            "contribucion_total": 79800
        },
        {
            "producto_id": "P02",
            "nombre_producto": "Torta de chocolate",
            "precio_venta": 3500,
            "costo_total_unit": 2100,
            "margen_abs_unit": 1400,
            "margen_pct": 0.4,
            "unidades": 45,
            "contribucion_total": 63000
        },
        {
            "producto_id": "P05",
            "nombre_producto": "Brownie",
            "precio_venta": 1200,
            "costo_total_unit": 680,
            "margen_abs_unit": 520,
            "margen_pct": 0.433,
            "unidades": 85,
            "contribucion_total": 44200
        }
    ],
    "bottom_risk": [
        {
            "producto_id": "P11",
            "nombre_producto": "Galletas con chocolate",
            "precio_venta": 1200,
            "costo_total_unit": 1450,
            "margen_abs_unit": -250,
            "margen_pct": -0.208,
            "unidades": 80,
            "perdida_total": -20000
        },
        {
            "producto_id": "P09",
            "nombre_producto": "Pan integral",
            "precio_venta": 2000,
            "costo_total_unit": 1950,
            "margen_abs_unit": 50,
            "margen_pct": 0.025,
            "unidades": 200,
            "contribucion_total": 10000
        }
    ]
}

# HISTORY 2: Tiempo vs margen
STORY_2_DATA = {
    "story_id": 2,
    "title": "Tiempo de producción vs Margen",
    "subtitle": "¿Qué productos me quitan mucho tiempo con poco retorno?",
    "empresa": "Panadería Demo",
    "rubro": "Alimentos",
    "thresholds": {
        "esfuerzo_alto_minutos": 300,
        "margen_bajo_pct": 0.15
    },
    "items": [
        {
            "servicio_id": "P04",
            "nombre_servicio": "Muffin vainilla",
            "minutos_trabajo": 45,
            "margen_pct": 0.472,
            "margen_abs": 850,
            "categoria": "eficiente"
        },
        {
            "servicio_id": "P02",
            "nombre_servicio": "Torta de chocolate",
            "minutos_trabajo": 180,
            "margen_pct": 0.4,
            "margen_abs": 1400,
            "categoria": "eficiente"
        },
        {
            "servicio_id": "P11",
            "nombre_servicio": "Galletas con chocolate",
            "minutos_trabajo": 120,
            "margen_pct": -0.208,
            "margen_abs": -250,
            "categoria": "alto_esfuerzo_bajo_retorno"
        },
        {
            "servicio_id": "P09",
            "nombre_servicio": "Pan integral",
            "minutos_trabajo": 240,
            "margen_pct": 0.025,
            "margen_abs": 50,
            "categoria": "alto_esfuerzo_bajo_retorno"
        },
        {
            "servicio_id": "P07",
            "nombre_servicio": "Alfajor",
            "minutos_trabajo": 30,
            "margen_pct": 0.422,
            "margen_abs": 380,
            "categoria": "eficiente"
        }
    ]
}

# HISTORY 3: Alertas simples
STORY_3_DATA = {
    "story_id": 3,
    "title": "Alertas de rentabilidad",
    "subtitle": "Productos con problemas que requieren acción",
    "empresa": "Panadería Demo",
    "rubro": "Alimentos",
    "alerts": [
        {
            "alert_id": "A-001",
            "servicio_id": "P11",
            "nombre_servicio": "Galletas con chocolate",
            "tipo": "MARGEN_NEGATIVO",
            "severidad": "CRITICA",
            "explicacion_breve": "Este producto está generando pérdidas. El costo unitario (1450) supera el precio de venta (1200).",
            "accion_sugerida": "Aumentar precio, reducir costos de insumos o descontinuar el producto.",
            "impacto_estimado": {
                "margen_actual": -0.208,
                "perdida_total_periodo": -20000,
                "margen_objetivo": 0.25
            }
        },
        {
            "alert_id": "A-002",
            "servicio_id": "P09",
            "nombre_servicio": "Pan integral",
            "tipo": "MARGEN_CRITICO",
            "severidad": "ALTA",
            "explicacion_breve": "Margen muy bajo (2.5%) a pesar de alta demanda (200 unidades). El tiempo invertido no justifica el retorno.",
            "accion_sugerida": "Renegociar precio con clientes o revisar eficiencia de producción.",
            "impacto_estimado": {
                "margen_actual": 0.025,
                "contribucion_total_actual": 10000,
                "potencial_si_margen_20pct": 40000
            }
        },
        {
            "alert_id": "A-003",
            "servicio_id": "P07",
            "nombre_servicio": "Alfajor",
            "tipo": "EFICIENCIA",
            "severidad": "MEDIA",
            "explicacion_breve": "Producto rentable pero con variación en tiempos de producción. Oportunidad de optimización.",
            "accion_sugerida": "Analizar si hay mejoras en el proceso o si es por variabilidad inherente.",
            "impacto_estimado": {
                "margen_actual": 0.422,
                "potencial_mejora": "5-10% optimización de tiempo"
            }
        }
    ]
}

# HISTORY 4: Drivers de costos
STORY_4_DATA = {
    "story_id": 4,
    "title": "Drivers de costos - ¿Dónde enfocar ajustes?",
    "subtitle": "Identificar qué costos impactan más tu negocio",
    "empresa": "Panadería Demo",
    "rubro": "Alimentos",
    "top_insumos": [
        {
            "insumo": "Harina",
            "impacto_total": 145000,
            "variacion_pct": 0.12,
            "observacion": "Sube producto principal"
        },
        {
            "insumo": "Azúcar",
            "impacto_total": 98000,
            "variacion_pct": 0.08,
            "observacion": "Bajo variación"
        },
        {
            "insumo": "Mantequilla",
            "impacto_total": 76000,
            "variacion_pct": 0.15,
            "observacion": "Alta volatilidad"
        },
        {
            "insumo": "Huevos",
            "impacto_total": 54000,
            "variacion_pct": 0.22,
            "observacion": "Muy volátil, considerar proveedores"
        }
    ],
    "top_gastos_indirectos": [
        {
            "gasto": "Alquiler local",
            "monto_mensual": 150000,
            "porcentaje_costo_total": 0.18
        },
        {
            "gasto": "Energía eléctrica",
            "monto_mensual": 45000,
            "porcentaje_costo_total": 0.05
        },
        {
            "gasto": "Mano de obra fija",
            "monto_mensual": 200000,
            "porcentaje_costo_total": 0.24
        }
    ],
    "drivers_por_producto": [
        {
            "producto_id": "P02",
            "nombre_producto": "Torta de chocolate",
            "drivers_unitarios": [
                {
                    "insumo": "Harina",
                    "impacto_unit": 450,
                    "porcentaje_costo": 0.21
                },
                {
                    "insumo": "Azúcar",
                    "impacto_unit": 380,
                    "porcentaje_costo": 0.18
                },
                {
                    "insumo": "Mantequilla",
                    "impacto_unit": 520,
                    "porcentaje_costo": 0.25
                }
            ]
        },
        {
            "producto_id": "P04",
            "nombre_producto": "Muffin vainilla",
            "drivers_unitarios": [
                {
                    "insumo": "Harina",
                    "impacto_unit": 280,
                    "porcentaje_costo": 0.29
                },
                {
                    "insumo": "Huevos",
                    "impacto_unit": 180,
                    "porcentaje_costo": 0.19
                },
                {
                    "insumo": "Azúcar",
                    "impacto_unit": 240,
                    "porcentaje_costo": 0.25
                }
            ]
        }
    ],
    "accion_sugerida": "Enfocarse en negociar precio de harina y huevos, que juntos representan el 50% del costo directo."
}

# STORY 5: Sensibilidad de costos (Agente A - Costos)
STORY_5_DATA = {
    "story_id": 5,
    "title": "Análisis de sensibilidad - Drivers de costos",
    "subtitle": "Agente A: Impacto de cambios en insumos",
    "empresa": "Panadería Demo",
    "sensibilidad_productos": [
        {
            "producto_id": "P04",
            "nombre_producto": "Muffin vainilla",
            "margen_actual_pct": 0.472,
            "sensibilidades": [
                {
                    "insumo": "Harina",
                    "porcentaje_actual_costo": 0.29,
                    "impacto_si_sube_10pct": {
                        "costo_adicional_unit": 28,
                        "nuevo_margen_pct": 0.442,
                        "impacto_contribucion_500u": -14000
                    }
                },
                {
                    "insumo": "Huevos",
                    "porcentaje_actual_costo": 0.19,
                    "impacto_si_sube_10pct": {
                        "costo_adicional_unit": 18,
                        "nuevo_margen_pct": 0.453,
                        "impacto_contribucion_500u": -9000
                    }
                }
            ]
        },
        {
            "producto_id": "P02",
            "nombre_producto": "Torta de chocolate",
            "margen_actual_pct": 0.4,
            "sensibilidades": [
                {
                    "insumo": "Harina",
                    "porcentaje_actual_costo": 0.21,
                    "impacto_si_sube_10pct": {
                        "costo_adicional_unit": 45,
                        "nuevo_margen_pct": 0.368,
                        "impacto_contribucion_200u": -9000
                    }
                },
                {
                    "insumo": "Mantequilla",
                    "porcentaje_actual_costo": 0.25,
                    "impacto_si_sube_10pct": {
                        "costo_adicional_unit": 52,
                        "nuevo_margen_pct": 0.363,
                        "impacto_contribucion_200u": -10400
                    }
                }
            ]
        }
    ],
    "gastos_indirectos": [
        {
            "gasto": "Alquiler local",
            "monto_mensual": 150000,
            "impacto_por_unidad_promedio": 15.8,
            "urgencia": "FIJA"
        },
        {
            "gasto": "Mano de obra",
            "monto_mensual": 200000,
            "impacto_por_unidad_promedio": 21.0,
            "urgencia": "VARIABLE",
            "oportunidad": "Optimizar procesos"
        }
    ],
    "accion_sugerida": "Harina y mantequilla son críticos. Negociar contratos a largo plazo para fijar precios."
}

# STORY 6: Recomendaciones de Pricing (Agente 2)
STORY_6_DATA = {
    "story_id": 6,
    "title": "Recomendaciones de Pricing & Estrategia",
    "subtitle": "Agente 2: Impacto económico de cambios de precio",
    "empresa": "Panadería Demo",
    "recomendaciones": [
        {
            "producto_id": "P11",
            "nombre_producto": "Galletas con chocolate",
            "prioridad": 1,
            "impacto_economico": 20000,
            "problematica": "MARGEN NEGATIVO",
            "precio_actual": 1200,
            "costo_actual": 1450,
            "estrategia": "AUMENTAR PRECIO URGENTE",
            "opciones": [
                {
                    "escenario": "Aumentar 20% (1200 → 1440)",
                    "nuevo_margen_pct": 0.008,
                    "impacto_contribucion": -2000,
                    "demanda_elasticidad": "Riesgo: baja demanda 15%"
                },
                {
                    "escenario": "Reducir costo (negociar insumos)",
                    "nuevo_costo_unit": 1300,
                    "nuevo_margen_pct": 0.077,
                    "impacto_contribucion": 6000
                }
            ]
        },
        {
            "producto_id": "P09",
            "nombre_producto": "Pan integral",
            "prioridad": 2,
            "impacto_economico": 30000,
            "problematica": "MARGEN CRÍTICO",
            "precio_actual": 2000,
            "costo_actual": 1950,
            "estrategia": "AUMENTAR PRECIO O REDUCIR VOLUMEN",
            "opciones": [
                {
                    "escenario": "Aumentar 15% (2000 → 2300)",
                    "nuevo_margen_pct": 0.180,
                    "impacto_contribucion": 30000,
                    "demanda_elasticidad": "Si demanda cae 20%, aún +9000"
                },
                {
                    "escenario": "Optimizar procesos (-10% tiempo)",
                    "nuevo_costo_unit": 1880,
                    "nuevo_margen_pct": 0.060,
                    "impacto_contribucion": 12000
                }
            ]
        },
        {
            "producto_id": "P04",
            "nombre_producto": "Muffin vainilla",
            "prioridad": 3,
            "impacto_economico": 15000,
            "problematica": "OPORTUNIDAD DE CRECIMIENTO",
            "precio_actual": 1800,
            "costo_actual": 950,
            "estrategia": "OPTIMIZAR MARKETING/PRODUCCIÓN",
            "opciones": [
                {
                    "escenario": "Aumentar volumen 30% (120→156 unidades)",
                    "nuevo_impacto_contribucion": 31800,
                    "requerimiento": "Capacidad de producción disponible"
                },
                {
                    "escenario": "Aumentar precio 10% (1800 → 1980)",
                    "nuevo_margen_pct": 0.495,
                    "impacto_contribucion": 10800,
                    "demanda_elasticidad": "Bajo riesgo con marca consolidada"
                }
            ]
        }
    ],
    "resumen_prioridades": [
        {
            "rango": 1,
            "accion": "Galletas: Resolver margen negativo (20k impacto)",
            "urgencia": "CRÍTICA"
        },
        {
            "rango": 2,
            "accion": "Pan integral: Aumentar precio 15% o reducir (30k impacto)",
            "urgencia": "ALTA"
        },
        {
            "rango": 3,
            "accion": "Muffin: Crecer volumen o precio (15k oportunidad)",
            "urgencia": "MEDIA"
        }
    ]
}

