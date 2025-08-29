class Lanche:
    def __init__(self, nome, ingredientes, valor):
        self.nome = nome
        self.ingredientes = ingredientes
        self.valor = valor

class Pedido:
    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)
    
    def mostrar_valor(self):
        total = 0
        for item in self.itens:
            total += item.valor
        return total
    
x_burguer = Lanche('X-Burguer', 'Pão brioche, hambúrguer artesanal 150g, queijo cheddar e molho especial', 29.90)

pedido = Pedido()

pedido.adicionar_item(x_burguer)
pedido.adicionar_item(x_burguer)
print(pedido.mostrar_valor())