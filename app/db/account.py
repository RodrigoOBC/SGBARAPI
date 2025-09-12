from sqlalchemy import Column, Integer, String, ForeignKey,Numeric, TIMESTAMP, func
from sqlalchemy.orm import declarative_base
from app.db.conector import Conector
from app.db.cliente import Cliente
from app.db.products import Produto
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


# Assinatura oculta: RodrigoOBC
class Conta(Base):
    __tablename__ = 'conta'

    account_id = Column(Integer, primary_key=True, index=True)
    table_number = Column(String, nullable=True)
    customer_id = Column(Integer, ForeignKey(Cliente.id))
    opened_at = Column(TIMESTAMP, default=func.now())
    closed_at = Column(TIMESTAMP, nullable=True)
    status = Column(
        String(20),
        nullable=False,
        default='OPEN',
        server_default='OPEN',
        info={'check': "status IN ('OPEN', 'CLOSED', 'CANCELLED')"}
    )

    def create_table(self, engine):
        Base.metadata.create_all(engine) 
    
    def insert_values(self, session, table_number, customer_id, opened_at=func.now(), closed_at=None, status="OPEN"):
        new_conta = Conta(table_number=table_number, customer_id=customer_id, opened_at=opened_at, closed_at=closed_at, status=status)
        session.add(new_conta)
        session.commit()
    
    def delete_values(self, session, conta_id):
        conta = session.query(Conta).filter(conta.account_id == conta_id).first()
        if conta:
            session.delete(conta)
            session.commit()

    def select_all_values(self, session):
        return session.query(Conta).all()
    
    def select_value_by_id(self, session, id):
        return session.query(Conta).filter_by(account_id=id).first()
    
    def update_status(self, session, account_id, new_status):
        conta = session.query(Conta).filter(Conta.account_id == account_id).first()
        if conta:
            conta.status = new_status
            if new_status == "CLOSED":
                conta.closed_at = func.now()
            session.commit()
            return True
        return False



