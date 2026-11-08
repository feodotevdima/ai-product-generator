from typing import Any

from application.dto.product import Product
from application.interfaces.product_normalizer_interface import (
    ProductNormalizerInterface,
)


class ProductNormalizer(ProductNormalizerInterface):

    def normalize(self, data: dict[str, Any]) -> Product:
        name = self._get_value(
            data,
            "name",
            "product_name",
            "title",
            "model",
        )

        manufacturer = self._get_value(
            data,
            "manufacturer",
            "vendor",
            "brand",
        )

        description = self._get_value(
            data,
            "description",
            "type_prefix",
            "typePrefix",
            "product_type",
        )

        identifiers = self._normalize_identifiers(data)
        specs = self._normalize_specs(data)

        commercial_data = self._normalize_commercial_data(data)

        return Product(
            name=name,
            manufacturer=manufacturer,
            description=description,
            specs=specs,
            identifiers=identifiers,
            commercial_data=commercial_data,
            url=self._get_value(data, "url", "link"),
            picture=self._get_value(data, "picture", "image"),
        )

    @staticmethod
    def _get_value(
        data: dict[str, Any],
        *keys: str,
    ) -> Any:
        for key in keys:
            value = data.get(key)

            if value is not None and value != "":
                return value

        return None

    def _normalize_identifiers(
        self,
        data: dict[str, Any],
    ) -> dict[str, str]:
        identifiers = {}

        params = data.get("params", {})

        if isinstance(params, dict):
            for key, value in params.items():
                if key.lower() in {
                    "артикул",
                    "код товара",
                    "код производителя",
                }:
                    identifiers[key] = str(value)

        elif isinstance(params, list):
            for param in params:
                if not isinstance(param, dict):
                    continue

                name = param.get("name")
                value = param.get("value")

                if name and value is not None:
                    if name.lower() in {
                        "артикул",
                        "код товара",
                        "код производителя",
                    }:
                        identifiers[name] = str(value)

        existing = data.get("identifiers")

        if isinstance(existing, dict):
            identifiers.update(
                {str(key): str(value) for key, value in existing.items()}
            )

        vendor_code = self._get_value(
            data,
            "vendor_code",
            "vendorCode",
            "manufacturer_code",
        )

        if vendor_code is not None:
            identifiers.setdefault(
                "Код производителя",
                str(vendor_code),
            )

        return identifiers

    def _normalize_specs(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        specs = {}

        source_specs = self._get_value(
            data,
            "specs",
            "specifications",
            "characteristics",
        )

        if isinstance(source_specs, dict):
            specs.update(source_specs)

        params = data.get("params", {})

        identifier_names = {
            "артикул",
            "код товара",
            "код производителя",
        }

        if isinstance(params, dict):
            for key, value in params.items():
                if key.lower() not in identifier_names:
                    specs.setdefault(key, value)

        elif isinstance(params, list):
            for param in params:
                if not isinstance(param, dict):
                    continue

                name = param.get("name")
                value = param.get("value")

                if name and name.lower() not in identifier_names and value is not None:
                    specs.setdefault(name, value)

        return specs

    def _normalize_commercial_data(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        commercial_data = {}

        source_data = data.get("commercial_data")

        if isinstance(source_data, dict):
            commercial_data.update(source_data)

        price = self._get_value(data, "price")
        currency = self._get_value(
            data,
            "currency",
            "currency_id",
            "currencyId",
        )
        available = self._get_value(data, "available", "in_stock")

        if price is not None:
            commercial_data["price"] = price

        if currency is not None:
            commercial_data["currency"] = currency

        if available is not None:
            commercial_data["available"] = available

        return commercial_data
