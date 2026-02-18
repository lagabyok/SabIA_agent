import os
import logging
from typing import Dict, Any
from google import genai
from .base import LLMProvider
from .prompts import executive_report_prompt

logger = logging.getLogger(__name__)


class GeminiProvider(LLMProvider):
    def __init__(self) -> None:
        # 1. Verificacion de variables de entorno
        self.api_key = os.getenv("GEMINI_API_KEY")
        # Usar un modelo disponible segun /llm/gemini/models
        self.model_name = os.getenv("GEMINI_MODEL", "models/gemini-flash-latest")

        logger.info(f"Inicializando GeminiProvider - API Key presente: {bool(self.api_key)}")

        if not self.api_key:
            logger.error("No se encontro GEMINI_API_KEY en el entorno")
            self.client = None
            return

        try:
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Cliente Gemini instanciado con modelo: {self.model_name}")
        except Exception as e:
            logger.error(f"Error critico al instanciar el cliente: {str(e)}")
            self.client = None

    def generate_executive_report(self, payload: Dict[str, Any]) -> str:
        logger.info("=== INICIANDO GENERACION DE REPORTE CON GEMINI ===")

        if not self.client:
            logger.warning("Cliente no disponible, devolviendo respuesta por defecto")
            return self._get_fallback_response()

        try:
            prompt = executive_report_prompt(payload)
            logger.info(f"Llamando a Gemini API ({self.model_name})...")

            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )

            if response and response.text:
                logger.info("Respuesta recibida exitosamente")
                return response.text

            raise ValueError("La respuesta de Gemini vino vacia")
        except Exception as e:
            logger.error(f"ERROR al llamar a Gemini: {type(e).__name__}: {str(e)}")
            import traceback
            logger.error(f"Traceback:\n{traceback.format_exc()}")
            return self._get_error_response(e, payload)

    def list_available_models(self) -> Dict[str, Any]:
        if not self.client:
            return {"ok": False, "models": [], "error": "Cliente Gemini no disponible"}

        try:
            models_iter = self.client.models.list()
            models = []
            for model in models_iter:
                name = getattr(model, "name", None) or getattr(model, "id", None)
                if name:
                    models.append(name)
            return {"ok": True, "models": models}
        except Exception as e:
            return {"ok": False, "models": [], "error": f"{type(e).__name__}: {str(e)}"}

    def _get_fallback_response(self) -> str:
        return (
            "### Resumen\n"
            "- Se detectaron oportunidades de mejora en margen y eficiencia.\n\n"
            "### Alertas clave\n"
            "- Priorizar productos con margen negativo.\n"
        )

    def _get_error_response(self, e: Exception, payload: Dict[str, Any]) -> str:
        return (
            "### Error al generar reporte\n"
            f"- Detalle: {str(e)}\n\n"
            "### Resumen alternativo\n"
            f"- Alertas procesadas: {len(payload.get('alerts', []))}\n"
        )
