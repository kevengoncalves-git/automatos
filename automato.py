print("-"*50)
print("Bem vindo ao conversor e validador de autômatos")
print("-"*50)

print()

print("-"*50)
print("Vamos formalizar o seu AFND")
print("-"*50)


alfabeto = input("Insira o alfabeto do seu autômato(separe os simbolos por vírgula): ")

simbolos = set(alfabeto.split(",")) #retira as vírgulas e cria um conjunto com os símbolos
lista_simbolos = set()#cria um conjunto vazio para armazenar os símbolos

for simbolo in simbolos:
    simbolo = simbolo.strip() #retira possiveis espaços em branco
    lista_simbolos.add(simbolo)

print("Seu alfabeto é: ", sorted(lista_simbolos))
print()

estados = input("Insira os estados do seu autômato(separe os estados por vírgula): ")
estados = estados.split(",") #retira as vírgulas e cria uma lista com os estados
lista_estados = set()
for estado in estados:
    estado = estado.strip() #retira possiveis espaços em branco
    lista_estados.add(estado)
print("Seus estados são: ", sorted(lista_estados))
print()

estados_finais = input("Insira os estados finais do seu autômato(separe os estados por vírgula): ")
estados_finais = estados_finais.split(",") #retira as vírgulas e cria uma lista com os estados finais
lista_estados_finais = set() #retira as vírgulas e cria um conjunto com os estados finais

for estado_final in estados_finais:
    estado_final = estado_final.strip() #retira possiveis espaços em branco
    lista_estados_finais.add(estado_final)

print("Seus estados finais são: ", sorted(lista_estados_finais))

estado_inicial = 'q0'

funcao_transicao = {}
#Cria a estrutura inicial da função de transição
for estado in sorted(lista_estados):
    funcao_transicao[estado] = { #estado como chave principal
        simbolo: list() for simbolo in sorted(lista_simbolos) #simbolos como chaves secundárias : valores vazios (listas)   
    }

def inserir_transicao(estado_atual):
    #Verifica se o estado atual está na função de transição
    if estado_atual in funcao_transicao:
        #Percorre os simbolos do estado atual
        for simbolo in funcao_transicao[estado_atual].keys():
            #Processamento pra retirar a virgula e os espaços em branco
            destinos = input(f"Insira os estados de destino para a transição do estado '{estado_atual}' com o símbolo '{simbolo}' (separe os estados por vírgula ou deixe vazio se não houver transição): ")
            destinos = destinos.split(",") if destinos else []
            destinos_processados = list()
            for destino in destinos:
                destino = destino.strip()
                #Verifica se o destino existe na lista de estados
                if destino in lista_estados:
                    destinos_processados.append(destino)
                elif destino != '':
                    print(f"Aviso: O estado '{destino}' não é válido e será ignorado.")
            funcao_transicao[estado_atual][simbolo] = destinos_processados #Anexa os destinos a chave secundaria

inserir_transicao('q0')

print(funcao_transicao)
