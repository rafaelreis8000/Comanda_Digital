from sqlalchemy import create_engine, Integer, String, Float, Column
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

engine = create_engine('sqlite:///Proj_Lanches/database.db', echo = True)

Base = declarative_base()

class Lanche(Base):
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)
    description = Column(String, nullable = False)
    value = Column(Float, nullable = False)

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key = True)
    itens = Column()