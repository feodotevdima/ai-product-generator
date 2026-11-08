from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCard(BaseModel):
    """Сгенерированное содержимое товарной карточки."""

    model_config = ConfigDict(extra="forbid")

    seo_title: str = Field(max_length=70)
    seo_description: str

    key_characteristics: dict[str, str]

    search_queries: list[str] = Field(min_length=3, max_length=5)

    commercial_block: str

    warnings: list[str] = Field(default_factory=list)

    @field_validator("seo_title", "seo_description", "commercial_block")
    @classmethod
    def validate_not_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Поле не должно быть пустым.")
        return value

    @field_validator("search_queries")
    @classmethod
    def validate_search_queries(cls, value: list[str]) -> list[str]:
        if any(not query.strip() for query in value):
            raise ValueError("Поисковые запросы не должны быть пустыми.")
        return value
