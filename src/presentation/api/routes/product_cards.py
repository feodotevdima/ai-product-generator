from typing import Any

from fastapi import APIRouter

from application.dto.product import Product
from application.dto.product_card import ProductCard
from presentation.api.dependencies import ProductCardServiceDep, ProductNormalizerDep

router = APIRouter(
    prefix="/product-cards",
    tags=["Product cards"],
)


@router.post("/generate", response_model=ProductCard)
async def generate_product_card(
    data: dict[str, Any],
    service: ProductCardServiceDep,
    normalizer: ProductNormalizerDep,
) -> ProductCard:
    product: Product = normalizer.normalize(data)
    result = await service.generate_product_card(product)
    return result
