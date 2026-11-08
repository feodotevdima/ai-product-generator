import json
import logging

from pydantic import ValidationError

from application.dto.product import Product
from application.dto.product_card import ProductCard
from application.interfaces.llm_provider_interface import LLMProviderInterface
from application.interfaces.product_card_service_interface import (
    ProductCardServiceInterface,
)
from core.config import get_settings
from core.exceptions import LLMTransientError, ProductCardGenerationError
from core.prompts import SYSTEM_PROMPT

logger = logging.getLogger(__name__)

settings = get_settings()

MAX_ATTEMPTS = settings.MAX_ATTEMPTS


class ProductCardService(ProductCardServiceInterface):

    def __init__(
        self,
        llm_provider: LLMProviderInterface,
    ) -> None:
        self._llm_provider = llm_provider

    async def generate_product_card(self, product: Product) -> ProductCard:
        user_prompt = json.dumps(
            product.model_dump(mode="json"),
            ensure_ascii=False,
            indent=2,
        )

        retry_instruction = ""

        for attempt in range(1, MAX_ATTEMPTS + 1):
            current_prompt = user_prompt

            if retry_instruction:
                current_prompt += (
                    "\n\nДополнительные требования к генерации:\n"
                    f"{retry_instruction}"
                )

            result = None

            try:
                result = await self._llm_provider.generate_json(
                    system_prompt=SYSTEM_PROMPT,
                    user_prompt=current_prompt,
                )
                result["key_characteristics"] = self._get_characteristics(product)
                product_card = ProductCard.model_validate(result)
                return product_card

            except (
                LLMTransientError,
                ValidationError,
            ) as exc:
                if isinstance(exc, LLMTransientError):
                    retry_instruction = (
                        "Сформируй корректный JSON-объект в соответствии "
                        "со структурой и требованиями системного промпта. "
                        "Все обязательные поля должны присутствовать."
                    )
                elif isinstance(exc, ValidationError):
                    retry_instruction = "\n".join(
                        f"- {'.'.join(map(str, error['loc']))}: {error['msg']}"
                        for error in exc.errors(
                            include_input=False,
                            include_url=False,
                        )
                    )

                logger.warning(
                    "Генерация карточки не прошла проверку (попытка %s из %s): %s",
                    attempt,
                    MAX_ATTEMPTS,
                    retry_instruction,
                )

                if attempt == MAX_ATTEMPTS:
                    if result is not None:
                        logger.error(
                            "Последний ответ LLM:\n%s",
                            json.dumps(result, ensure_ascii=False, indent=2),
                        )

                    raise ProductCardGenerationError(
                        "Не удалось сгенерировать корректную карточку товара."
                    ) from exc

        raise ProductCardGenerationError(
            "Не удалось сгенерировать корректную карточку товара."
        )

    def _get_characteristics(self, product: Product) -> dict[str, str]:
        return {str(key): str(value) for key, value in product.specs.items()}
