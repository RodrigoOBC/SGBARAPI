from fastapi import APIRouter
from app.db.account import Conta
from app.services.account_service import account_service
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()
Conector_db = Conector(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
account_svc = account_service()

@router.get("")
async def get_all_accounts():
    db = Conector_db.conect()
    accounts = []
    conta = Conta()
    res = conta.select_all_values(db)
    for account in res:
        account_id = account.account_id
        accounts.append(account_svc.get_accounts_by_id(account_id))
    Conector_db.desconect()
    return accounts

@router.get("/{account_id}")
async def get_account_by_id(account_id: int):
    res = account_svc.get_accounts_by_id(account_id)
    return res

@router.post("")
async def create_account(request: dict):
    print(request)
    res = account_svc.create_account(request)
    return {"message": "Account created successfully"}

@router.put("/{account_id}/close")
async def close_account(account_id: int):
    res = account_svc.close_account(account_id)
    return res

@router.post('/add_item')
async def add_item(request: dict):
    res = account_svc.add_item_to_account(request)
    return res