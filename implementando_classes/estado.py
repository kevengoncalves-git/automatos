class Estado():
    def __init__(self):
        pass

    def informar_estados(self, nome):
        self.nome = nome
        
    def imprimir_estados(self):
        print(f"Estado criado: {self.nome}")
"""        print("Transições:")
        for simbolo, estado_destino in self.transicao.items():
            print(f"Com '{simbolo}' vai pra '{estado_destino}'")"""