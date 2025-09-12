# RodrigoOBC signature
from fastapi import APIRouter
from app.api.dashboard.client import router as client_router
from app.api.dashboard.product import router as product_router
from app.api.dashboard.account import router as account_router

router = APIRouter()

@router.get("/ping")
async def ping():
    return {"message": "pong"}

router.include_router(client_router, prefix="/clients", tags=["clients"])
router.include_router(product_router, prefix="/products", tags=["products"])
router.include_router(account_router, prefix="/accounts", tags=["accounts"])