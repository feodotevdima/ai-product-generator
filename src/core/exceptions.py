class AppError(Exception):
    """Базовое исключение приложения."""


class LLMProviderError(AppError):
    """Ошибка при обращении к LLM-провайдеру."""


class LLMTransientError(LLMProviderError):
    """Временная ошибка при обращении к LLM-провайдеру."""

    pass


class LLMFatalError(LLMProviderError):
    """Постоянная ошибка при обращении к LLM-провайдеру."""

    pass


class ProductCardGenerationError(AppError):
    """Ошибка при генерации карточки товара."""
