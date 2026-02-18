from typing import Dict, Any

def executive_report_prompt(payload: Dict[str, Any]) -> str:
    # Payload trae kpis + top alerts (ya calculados)
    k = payload.get("kpis", {})
    alerts = payload.get("alerts", [])[:5]

    lines = []
    lines.append("Redacta un reporte ejecutivo breve, accionable y explicable para una Pyme.")
    lines.append("No inventes números: usa solo los que aparecen en el JSON.")
    lines.append("\nKPIs:")
    lines.append(str(k))
    lines.append("\nTop alertas (máximo 5):")
    lines.append(str(alerts))
    lines.append("\nFormato de salida en markdown con secciones:")
    lines.append("### Resumen\n- ...\n### Alertas clave\n- ...\n### Acciones recomendadas\n- ...\n### Impacto estimado\n- ...")
    return "\n".join(lines)
