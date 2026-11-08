from abc import ABC, abstractmethod
from typing import Any

from application.dto.product import Product


class ProductNormalizerInterface(ABC):
    """Интерфейс нормализации входных данных о товарах."""

    @abstractmethod
    def normalize(
        self,
        data: dict[str, Any],
    ) -> Product:
        raise NotImplementedError
