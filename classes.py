from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

db = create_engine('sqlite:///D:\GitHub\Proj_Lanches/banco.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()

class PedidoLanche(Base):
    __tablename__ = 'pedido_lanches'
    id = Column(Integer, primary_key = True)
    pedido_id = Column(ForeignKey('pedidos.id'))
    lanche_id = Column(ForeignKey('lanches.id'))

class Lanche(Base):
    __tablename__ = 'lanches'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    valor = Column(Float, nullable = False)
    pedidos = relationship('Pedido', secondary = 'pedido_lanches', back_populates = 'lanches')

    def __init__(self, nome, valor):
        self.nome = nome
        self.valor = valor

    def cadastrar_lanche(nome, valor):
        session.add(Lanche(nome = nome, valor = valor))
        session.commit()

class Pedido(Base):
    __tablename__ = 'pedidos'
    id = Column(Integer, primary_key = True)
    data = Column(DateTime, nullable = False)
    cliente = Column(ForeignKey('clientes.id'))
    lanches = relationship('Lanche', secondary = 'pedido_lanches', back_populates = 'pedidos')

    def __init__(self, cliente, data, lanches):
        self.cliente = cliente
        self.data = data
        self.lanches = lanches
    
    def fazer_pedido(cliente, data, lanches_id):
        lanches = session.query(Lanche).filter(Lanche.id.in_(lanches_id)).all() #lê somente a ID de cada lanche para fazer o pedido
        session.add(Pedido(cliente = cliente, data = data, lanches = lanches))
        session.commit()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)

    def __init__(self, nome):
        self.nome = nome

    def cadastrar_cliente(nome):
        session.add(Cliente(nome = nome))
        session.commit()

Base.metadata.create_all(bind = db)

#Cliente.cadastrar_cliente('Giuseppe')
#Cliente.cadastrar_cliente('Josefa')
#Lanche.cadastrar_lanche('X-Burguer', 23.90)
#Lanche.cadastrar_lanche('X-Bacon', 27.90)