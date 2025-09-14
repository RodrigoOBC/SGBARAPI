from app.db.account import Conta
from app.db.account_product import Conta_produto
from app.db.products import Produto
from app.db.cliente import Cliente
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()

class account_service:
    def __init__(self):
        self.conector = Conector(os.getenv('DB_USER'), os.getenv('DB_PASSWORD'), os.getenv('DB_NAME'))
        self.conta = Conta()
        self.produto = Produto()
        self.cliente = Cliente()
        self.conta_produto = Conta_produto()
    
    def get_accounts_by_id(self, account_id):
        db = self.conector.conect()
        produtos =  self.get_itens_by_account_id(account_id)
        sum_total = self.get_sum_total_by_account_id(account_id)
        client_name = self.get_client_name_by_account_id(account_id)
        account = self.conta.select_value_by_id(db, account_id)
        accounts = {
            "account_id": account_id,
            "client_name": client_name.get("client_name"),
            "items": produtos,
            "sataus": account.status,
            "created_at": account.opened_at,
            "closed_at": account.closed_at,
            "total": sum_total.get("total")
        }
        self.conector.desconect()
        return accounts
        
    def sum_total_values(self,db, products_in_account):
        total = 0.00
        for item in products_in_account:
            product = self.produto.select_value_by_id(db, item.product_id)
            if product:
                total += float(product.value) * item.quantity
        return total

    def get_sum_total_by_account_id(self, account_id):
        db = self.conector.conect()
        products = self.conta_produto.select_value_by_account_id(db, account_id)
        total = self.sum_total_values(db, products)
        self.conector.desconect()
        return {
            "total": total
        }
    
    def get_itens_by_account_id(self, account_id):
        db = self.conector.conect()
        items = self.conta_produto.select_value_by_account_id(db, account_id)
        result = []
        for item in items:
            product = self.produto.select_value_by_id(db, item.product_id)
            if product:
                result.append({
                    "item_id": item.item_id,
                    "product_id": item.product_id,
                    "product_name": product.name,
                    "quantity": item.quantity,
                    "subtotal": float(product.value) * item.quantity,
                    "add_at": item.add_at
                })
        self.conector.desconect()
        return result
    
    def get_client_name_by_account_id(self, account_id):
        db = self.conector.conect()
        account = self.conta.select_value_by_id(db, account_id)
        if not account:
            self.conector.desconect()
            return {"error": "Account not found"}
        
        client = self.cliente.select_value_by_id(db, account.customer_id)
        self.conector.desconect()
        if client:
            return {"client_name": client.name}
        else:
            return {"error": "Client not found"}
    
    def get_count_by_customer_id(self, customer_id):
        
        return {"total_accounts": accounts}
    
    def create_account(self, account_object):
        print()
        db = self.conector.conect()
        self.conta.insert_values(db,account_object['table_number'], account_object['customer_id'])
        self.conector.desconect()
        return {"message": "Account created successfully"}
    
    def close_account(self, account_id):
        db = self.conector.conect()
        account = self.conta.select_value_by_id(db, account_id)
        if not account:
            self.conector.desconect()
            return {"error": "Account not found"}
        if account.status == "CLOSED":
            self.conector.desconect()
            return {"error": "Account is already closed"}
        
        total = self.get_sum_total_by_account_id(account_id).get("total", 0.00)
        self.conta.update_status(db, account_id, new_status="CLOSED")
        self.conector.desconect()
        return {"message": "Account closed successfully"}
    
    def add_item_to_account(self, request):
        db = self.conector.conect()
        account_id = request.get("account_id")
        product_id = request.get("product_id")
        quantity = request.get("quantity")
        
        account = self.conta.select_value_by_id(db, account_id)
        if not account:
            self.conector.desconect()
            return {"error": "Account not found"}
        if account.status == "CLOSED":
            self.conector.desconect()
            return {"error": "Cannot add items to a closed account"}
        
        product = self.produto.select_value_by_id(db, product_id)
        if not product:
            self.conector.desconect()
            return {"error": "Product not found"}
        
        self.conta_produto.insert_values(db, product_id, account_id, quantity)
        self.conector.desconect()
        return {"message": "Item added to account successfully"}