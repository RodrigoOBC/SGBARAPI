from fastapi import APIRouter
from app.db.products import Produto
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()
Conector_db = Conector(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))

@router.get("")
async def get_all_products():
    db = Conector_db.conect()
    produto = Produto()
    res = produto.select_all_values(db)
    Conector_db.desconect()
    return res

@router.get("/{product_id}")
async def get_product_by_id(product_id: int):
    db = Conector_db.conect()
    produto = Produto()
    res = produto.select_value_by_id(db, product_id)
    Conector_db.desconect()
    return res


@router.post("")
async def create_product(request: dict):
    db = Conector_db.conect()
    produto = Produto()
    produto.insert_values(db, request['name'], request['value'], request.get('quantity', 0))
    Conector_db.desconect()
    return {"message": "Product created successfully"}

@router.put("")
async def update_product(request: dict):
    db = Conector_db.conect()
    produto = Produto()
    updated_product = produto.update_value(db, request['id'], request.get('value'), request.get('quantity'))
    Conector_db.desconect()
    if updated_product:
        return {"message": f'product {updated_product.name} updated successfully'}
    else:
        return {"message": "Product not found"}


@router.delete("/{product_id}")
async def delete_product(product_id: int):
    print(f"Deleting product with ID: {product_id}")
    db = Conector_db.conect()
    produto = Produto()
    produto.delete_values(db, product_id)
    Conector_db.desconect()
    return {"message": "Product deleted successfully"}