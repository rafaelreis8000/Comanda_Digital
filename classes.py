from sqlalchemy import create_engine, Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
from datetime import datetime

db = create_engine('sqlite:///D:\GitHub\Proj_Lanches/bancodedados.db')
Session = sessionmaker(bind = db)
session = Session()

Base = declarative_base()

class PedidoLanche(Base):
    __tablename__ = 'pedido_lanche'

    id = Column(Integer, primary_key = True)
    pedido_id = Column('pedido_id', Integer, ForeignKey('pedidos.id'))
    lanche_id = Column('lanche_id', Integer, ForeignKey('lanches.id'))

class Lanche(Base):
    __tablename__ = 'lanches'

    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    descricao = Column(String)
    valor = Column(Float, nullable = False)
    pedidos = relationship('Pedido', secondary = 'pedido_lanche', back_populates = 'lanches')

    def __init__(self, nome, descricao, valor):
        self.nome = nome
        self.descricao = descricao
        self.valor = valor
    
    def criar_lanche(nome, descricao, valor):
        lanche = Lanche(nome = nome, descricao = descricao, valor = valor)
        session.add(lanche)
        session.commit()

class Pedido(Base):
    __tablename__ = 'pedidos'

    id = Column(Integer, primary_key = True)
    data = Column(DateTime)
    cliente_id = Column(ForeignKey('clientes.id'))
    lanches = relationship('Lanche', secondary = 'pedido_lanche', back_populates = 'pedidos')

    def __init__(self, data, cliente_id, lanches):
        self.data = data
        self.cliente_id = cliente_id
        self.lanches = lanches

    def fazer_pedido(data, cliente_id, lanches):
        pedido = Pedido(data = data, cliente_id = cliente_id, lanches = lanches)
        session.add(pedido)
        session.commit()

class Cliente(Base):
    __tablename__ = 'clientes'

    id = Column(Integer, primary_key = True)
    nome = Column(String, nullable = False)
    sobrenome = Column(String, nullable = False)
    telefone = Column(Integer, nullable = False)
    pedidos = relationship('Pedido')

    def __init__(self, nome, sobrenome, telefone):
        self.nome = nome
        self.sobrenome = sobrenome
        self.telefone = telefone
    
    def cadastrar_cliente(nome, sobrenome, telefone):
        cliente = Cliente(nome = nome, sobrenome = sobrenome, telefone = telefone)
        session.add(cliente)
        session.commit()
        

Base.metadata.create_all(db)

#Cliente.cadastrar_cliente('Giuseppe', 'Cadura', 12988765321)
#Cliente.cadastrar_cliente('Fernanda', 'Montenegro', 11988776655)

#Lanche.criar_lanche('X-Burguer', 'Pão brioche, hambúrguer de 150g, queijo cheddar e molho especial', 23.90)
#Lanche.criar_lanche('x_Bacon', 'pão brioche, hambúrguer de 150g, queijo cheddar, bacon e molho especial', 27.90)