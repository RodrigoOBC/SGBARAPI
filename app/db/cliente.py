from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from app.db.conector import Conector
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    telefone = Column(String, nullable=True)

    def create_table(self, engine):
        Base.metadata.create_all(engine) 
    
    def insert_values(self, session, client_name, client_telefone):
        new_cliente = Cliente(name=client_name, telefone=client_telefone)
        session.add(new_cliente)
        session.commit()
        return new_cliente.id
    
    def delete_values(self, session, cliente_id):
        cliente = session.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            session.delete(cliente)
            session.commit()

    def select_all_values(self, session):
        return session.query(Cliente).all()
    
    def select_value_by_id(self, session, id):
        return session.query(Cliente).filter_by(id=id).first()


if __name__ == "__main__":
    conector = Conector(
       user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    dbname=os.getenv("DB_NAME")
    )
    engine = conector.engine
    session = conector.session_local

    cliente = Cliente()
    cliente.create_table(engine)

    # Exemplo de inserção
    with session() as s:
        new_id = cliente.insert_values(s, "João Silva", "123456789")
        print(f"Novo cliente inserido com ID: {new_id}")

        # Exemplo de seleção
        all_clients = cliente.select_all_values(s)
        for client in all_clients:
            print(f"ID: {client.id}, Nome: {client.name}, Telefone: {client.telefone}")

        # Exemplo de seleção por ID
        client = cliente.select_value_by_id(s, new_id)
        if client: 
            print(f"Cliente encontrado - ID: {client.id}, Nome: {client.name}, Telefone:{client.telefone}")


