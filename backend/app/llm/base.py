from abc import ABC, abstractmethod
from typing import Dict, Any

class LLMProvider(ABC):
    @abstractmethod
    def generate_executive_report(self, payload: Dict[str, Any]) -> str:
        raise NotImplementedError
