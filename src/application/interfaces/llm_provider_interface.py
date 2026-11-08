from abc import ABC, abstractmethod
from typing import Any


class LLMProviderInterface(ABC):
    """Интерфейс для взаимодействия с провайдерами языковых моделей."""

    @abstractmethod
    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        raise NotImplementedError
