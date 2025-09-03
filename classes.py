from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

db = create_engine('sqlite:///D:\GitHub\Proj_Lanches/banco.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    sobrenome = Column(String, nullable = False)
    telefone = Column(Integer, nullable = False)

class LanchesPedidos(Base):
    __tablename__ = 'itens_pedidos'
    id = Column(Integer, primary_key = True)
    lanches_id = Column(ForeignKey('lanches.id'))
    pedidos_id = Column(ForeignKey('pedidos.id'))
    data = Column(DateTime, nullable = False)
    quantidade = Column(Integer, nullable = False)
    total = Column(Float, nullable = False)

class Lanche(Base):
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    descricao = Column(String)
    valor = Column(Float, nullable = False)
    pedidos = relationship('Pedido')

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(String, primary_key = True)
    cliente = Column(ForeignKey('clientes.id'))
    lanches = relationship('Lanche')

Base.metadata.create_all(bind = db)