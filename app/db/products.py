from sqlalchemy import Column, Integer, String, ForeignKey,Numeric
from sqlalchemy.orm import declarative_base
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


# CabralQA signature
class Produto(Base):
    __tablename__ = 'productos'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    value = Column(Numeric(10, 2), nullable=True)
    quantity = Column(Integer, nullable=True, default=0)

    def create_table(self, engine):
        Base.metadata.create_all(engine) 
    
    def insert_values(self, session, product_name, product_value, quantity=0):
        new_produto = Produto(name=product_name, value=product_value, quantity=quantity)
        session.add(new_produto)
        session.commit()
    
    def delete_values(self, session, producto_id):
        produto = session.query(Produto).filter(Produto.id == producto_id).first()
        if produto:
            session.delete(produto)
            session.commit()

    def select_all_values(self, session):
        return session.query(Produto).all()
    
    def select_value_by_id(self, session, id):
        return session.query(Produto).filter_by(id=id).first()

    def update_value(self, session, producto_id, new_value=None, new_quantity=None):
        produto = session.query(Produto).filter(Produto.id == producto_id).first()
        if produto:
            if new_value is not None:
                produto.value = new_value
            if new_quantity is not None:
                produto.quantity = new_quantity
            session.commit()
            session.refresh(produto)  # Atualiza a instância com os dados mais recentes do banco
        return produto

if __name__ == "__main__":
    conector = Conector(
       user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
    )
    engine = conector.engine
    session = conector.session_local

    produto = Produto()
    produto.create_table(engine)