from sqlalchemy import Column, Integer, String, ForeignKey,Numeric, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from app.db.conector import Conector
from app.db.account import Conta
from app.db.products import Produto
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class Conta_produto(Base):
    __tablename__ = 'contas_produtos'

    item_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey(Produto.id))
    account_id = Column(Integer, ForeignKey(Conta.account_id))
    quantity = Column(Integer, nullable=True, default=0)
    add_at = Column(TIMESTAMP, default=func.now())

    def create_table(self, engine):
        Base.metadata.create_all(engine) 
    
    def delete_table(self, engine):
        Base.metadata.drop_all(engine)
    
    def insert_values(self, session, product_id, account_id, quantity, add_at=func.now()):
        new_conta = Conta_produto(account_id=account_id, product_id=product_id, quantity=quantity, add_at=add_at)
        session.add(new_conta)
        session.commit()
    
    def delete_values(self, session, conta_id):
        conta = session.query(Conta_produto).filter(Conta_produto.account_id == conta_id).first()
        if conta:
            session.delete(conta)
            session.commit()

    def select_all_values(self, session):
        return session.query(Conta_produto).all()
    
    def select_value_by_id(self, session, id):
        return session.query(Conta_produto).filter_by(item_id=id).first()
    
    def select_value_by_account_id(self, session, account_id):
        return session.query(Conta_produto).filter_by(account_id=account_id).all()
    


if __name__ == "__main__":
    conector = Conector(
       user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
    )
    engine = conector.engine
    session = conector.session_local

    conta_produto = Conta_produto()
    conta_produto.create_table(engine)