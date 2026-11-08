from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends

from application.interfaces.llm_provider_interface import LLMProviderInterface
from application.interfaces.product_card_service_interface import (
    ProductCardServiceInterface,
)
from application.interfaces.product_normalizer_interface import (
    ProductNormalizerInterface,
)
from application.services.product_card_service import ProductCardService
from infrastructure.llm.open_router_provider import OpenRouterProvider
from presentation.normalization.product_normalizer import ProductNormalizer


async def get_llm_provider() -> AsyncIterator[LLMProviderInterface]:
    provider = OpenRouterProvider()

    try:
        yield provider
    finally:
        await provider.close()


LlmProviderDep = Annotated[LLMProviderInterface, Depends(get_llm_provider)]


def get_product_card_service(
    llm_provider: LLMProviderInterface = Depends(get_llm_provider),
) -> ProductCardServiceInterface:
    return ProductCardService(llm_provider=llm_provider)


ProductCardServiceDep = Annotated[
    ProductCardServiceInterface, Depends(get_product_card_service)
]


def get_product_normalizer() -> ProductNormalizer:
    return ProductNormalizer()


ProductNormalizerDep = Annotated[
    ProductNormalizerInterface, Depends(get_product_normalizer)
]
