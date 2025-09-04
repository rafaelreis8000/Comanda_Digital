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
    quantidade = Column(Integer, nullable = False, default = 1)

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

    def fazer_pedido(cliente, data, lancheid_quantidade):
        pedido = Pedido(cliente = cliente, data = data, lanches = [])
        session.add(pedido)
        session.flush()

        for lanche_id, qtd in lancheid_quantidade.items():
            session.add(PedidoLanche(pedido_id = pedido.id, lanche_id = lanche_id, quantidade = qtd))
        session.commit()

class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    sobrenome = Column(String, nullable = False)
    telefone = Column(Integer, nullable = False)

    def __init__(self, nome, sobrenome, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone

    def cadastrar_cliente(nome, sobrenome, telefone):
        session.add(Cliente(nome = nome, sobrenome = sobrenome, telefone = telefone))
        session.commit()

Base.metadata.create_all(bind = db)

def testar_cadastro():
    Cliente.cadastrar_cliente('Giuseppe', 'Cadura', 12999887675)
    Cliente.cadastrar_cliente('Pp', 'Marcondes', 1199876452)

    Lanche.cadastrar_lanche('X-Burguer', 23.90)
    Lanche.cadastrar_lanche('X-Bacon', 27.90)

    Pedido.fazer_pedido(1, datetime.today(), {1: 2, 2: 1})