import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from core.exceptions import LLMProviderError, ProductCardGenerationError
from presentation.api.routes.product_cards import router as product_cards_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)


app = FastAPI(
    title="AI Product Content Generator",
    version="1.0.0",
)


@app.exception_handler(ValidationError)
async def validation_exception_handler(
    request: Request,
    exc: ValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(include_url=False)},
    )


@app.exception_handler(LLMProviderError)
async def llm_provider_exception_handler(
    request: Request,
    exc: LLMProviderError,
):
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )


@app.exception_handler(ProductCardGenerationError)
async def product_card_exception_handler(
    request: Request,
    exc: ProductCardGenerationError,
):
    return JSONResponse(
        status_code=502,
        content={"detail": str(exc)},
    )


app.include_router(
    product_cards_router,
    prefix="/api",
)
