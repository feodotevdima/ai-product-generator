from abc import ABC, abstractmethod

from application.dto.product import Product
from application.dto.product_card import ProductCard


class ProductCardServiceInterface(ABC):
    """Интерфейс сервиса генерации содержимого товарных карточек."""

    @abstractmethod
    async def generate_product_card(
        self,
        product: Product,
    ) -> ProductCard:
        raise NotImplementedError
