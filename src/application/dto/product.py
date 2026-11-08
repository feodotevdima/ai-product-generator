from typing import Any

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator


class Product(BaseModel):
    """Исходные данные товара для генерации карточки."""

    model_config = ConfigDict(extra="forbid")

    name: str
    manufacturer: str
    description: str | None = None

    specs: dict[str, Any] = Field(default_factory=dict)
    identifiers: dict[str, str] = Field(default_factory=dict)

    commercial_data: dict[str, Any] = Field(default_factory=dict)

    url: HttpUrl | None = None
    picture: HttpUrl | None = None

    @field_validator("name", "manufacturer")
    @classmethod
    def validate_required_strings(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Поле не может быть пустым")

        return value

    @field_validator("description")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if value is not None:
            value = value.strip()

            if not value:
                return None

        return value
