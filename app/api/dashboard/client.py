from fastapi import APIRouter
from app.db.cliente import Cliente
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
Conector_db = Conector(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))

@router.get("")
async def get_all_client():
    db = Conector_db.conect()
    cliente = Cliente()
    res = cliente.select_all_values(db)
    Conector_db.desconect()
    return res

@router.get("/{client_id}")
async def get_client_by_id(client_id: int):
    db = Conector_db.conect()
    cliente = Cliente()
    res = cliente.select_value_by_id(db, client_id)
    Conector_db.desconect()
    return res

@router.post("")
async def create_client(resquest: dict):
    db = Conector_db.conect()
    cliente = Cliente()
    id = cliente.insert_values(db, resquest['name'], resquest['telefone'])
    Conector_db.desconect()
    return {"message": "Client created successfully", "id": id}
