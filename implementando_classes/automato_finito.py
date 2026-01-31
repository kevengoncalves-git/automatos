from estado import Estado

class Automato():
    def __init__(self):
       pass 

    def printar_alfabeto(self, lista_simbolos):
        print("Seu alfabeto: ")
        for simbolo in lista_simbolos:
            print(simbolo, end=' ')
        print("\n"+"-"*50)
    
    def printar_formalizacao(tupla_formalizacao):
        print("-"*50)
        print("Formalização do autômato:")
        print(f"M = (Q, Σ, δ, q0, F)\n")
        print(f"Onde:\nQ = {tupla_formalizacao[0]}\n")
        print(f"Σ = {tupla_formalizacao[1]}\n")
        print(f"δ = δ_{tupla_formalizacao[2]} \n")
        print(f"q0 = {tupla_formalizacao[3]}\n")
        print(f"F = {tupla_formalizacao[4]}\n")
        print("-"*50)

    def organizar_entrada(self, entrada):
        self.entrada = entrada.split(",") #retira as vírgulas e cria um conjunto com os elementos
        elementos_processados = list() #cria um conjunto vazio para armazenar os elementos
        for elemento in self.entrada:
            elemento = elemento.strip()
            elementos_processados.append(elemento)
        return elementos_processados
        
    def definir_automato(self):
        alfabeto = input("Insira o alfabeto do seu autômato(separe os simbolos por vírgula): ")
        self.alfabeto = alfabeto
        lista_simbolos = tuple(self.organizar_entrada(alfabeto))
        self.printar_alfabeto(lista_simbolos)

        estados = input("Insira os estados do seu autômato(separe os estados por vírgula): ")
        lista_estados = tuple(self.organizar_entrada(estados))
        for estado_nome in lista_estados:
            estado = Estado()
            estado.informar_estados(estado_nome)
            estado.imprimir_estados()

        #estados_finais = input("Insira os estados finais do seu autômato(separe os estados por vírgula): ")
        #lista_estados_finais = tuple(organizar_entrada(estados_finais))

