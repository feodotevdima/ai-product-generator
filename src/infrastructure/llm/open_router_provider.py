import json
import logging
from typing import Any

from openai import APIStatusError, AsyncOpenAI, OpenAIError

from application.interfaces.llm_provider_interface import LLMProviderInterface
from core.config import get_settings
from core.exceptions import LLMFatalError, LLMTransientError

settings = get_settings()

logger = logging.getLogger(__name__)


class OpenRouterProvider(LLMProviderInterface):

    def __init__(
        self,
        api_key: str = settings.OPENROUTER_API_KEY,
        model: str = settings.OPENROUTER_MODEL,
        base_url: str = settings.OPENROUTER_BASE_URL,
    ) -> None:
        self._model = model

        self._client = AsyncOpenAI(
            api_key=api_key,
            base_url=base_url,
            timeout=60.0,
            max_retries=2,
        )

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> dict[str, Any]:

        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                response_format={"type": "json_object"},
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    },
                ],
            )
        except APIStatusError as exc:
            logger.error(
                "Ошибка OpenRouter API: status=%s, response=%s",
                exc.status_code,
                exc.response.text,
            )

            if exc.status_code == 429 or exc.status_code >= 500:
                raise LLMTransientError("Временная ошибка LLM-провайдера.") from exc

            raise LLMFatalError("Ошибка при обращении к LLM-провайдеру.") from exc
        except OpenAIError as exc:
            logger.exception("Ошибка OpenAI SDK")
            raise LLMFatalError("Ошибка при обращении к LLM-провайдеру.") from exc

        if not response.choices:
            raise LLMTransientError("LLM вернула пустой ответ.")

        content = response.choices[0].message.content

        if not content:
            raise LLMTransientError("LLM вернула пустой ответ.")

        try:
            result = json.loads(content)

        except json.JSONDecodeError as exc:
            raise LLMTransientError("LLM вернула некорректный JSON.") from exc

        if not isinstance(result, dict):
            raise LLMTransientError("Ответ LLM должен быть JSON-объектом.")

        return result

    async def close(self) -> None:
        await self._client.close()
