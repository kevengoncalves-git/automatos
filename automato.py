print("-"*50)
print("Bem vindo ao conversor e validador de autômatos")
print("-"*50)

print()

print("-"*50)
print("Vamos formalizar o seu AFND")
print("-"*50)

def organizar_entrada(entrada):
    elementos = entrada.split(",") #retira as vírgulas e cria um conjunto com os elementos
    elementos_processados = list() #cria um conjunto vazio para armazenar os elementos
    for elemento in elementos:
        elemento = elemento.strip()
        elementos_processados.append(elemento)
    return elementos_processados

alfabeto = input("Insira o alfabeto do seu autômato(separe os simbolos por vírgula): ")
lista_simbolos = tuple(organizar_entrada(alfabeto))

print(f"Seu alfabeto é: {lista_simbolos}\n")

estados = input("Insira os estados do seu autômato(separe os estados por vírgula): ")
lista_estados = tuple(organizar_entrada(estados))

print(f"Seus estados são: {lista_estados}\n")
print()

estados_finais = input("Insira os estados finais do seu autômato(separe os estados por vírgula): ")
lista_estados_finais = tuple(organizar_entrada(estados_finais))

print(f"Seus estados finais são: {lista_estados_finais}\n")

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
            print("-"*50)
            print(f"--> Trabalhando com o estado {estado_atual}")
            destinos = input(f"Insira os estados de destino o estado '{estado_atual}' com o símbolo '{simbolo}' (deixe vazio se não houver transição): ")
            print("-"*50)
            print("\n")
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

for estado in lista_estados:
    inserir_transicao(estado)

print("Função de transição final do AFND:")
for estado, simbolo in funcao_transicao.items():
    print(f"Estado: {estado}")
    for chave, destinos in simbolo.items():
        print(f"Símbolo: {chave} | Destinos: {destinos}")
    print("-"*30)

while True:
    resposta = input("Deseja verificar uma palavra no AFND? (s/n): ").strip().lower()
    if resposta == 'n':
        break
    if resposta != 's':
        print("Resposta inválida. Digite 's' ou 'n'.\n")
        continue

    print("Iniciando verificação da palavra...\n")
    palavra = input("Insira a palavra que deseja verificar no AFND: ")

    estado_atual_lido = estado_inicial
    estados_percorridos = [estado_atual_lido]

    for i, simbolo in enumerate(palavra):

        if simbolo not in lista_simbolos:
            print(f"A palavra é inválida! O símbolo '{simbolo}' na posição {i} não pertence ao alfabeto.")
            break

        cabeca_de_leitura = i
        estados_de_destino = funcao_transicao[estado_atual_lido][simbolo]
        estado_atual_lido = estados_de_destino[0] if estados_de_destino else None

        estados_percorridos.append(estado_atual_lido)

        if cabeca_de_leitura == len(palavra) - 1:
            if estado_atual_lido in lista_estados_finais:
                print(f"A palavra '{palavra}' é aceita pelo AFND! Estado final alcançado: '{estado_atual_lido}'")
            else:
                print(f"A palavra '{palavra}' é rejeitada pelo AFND! Estado final alcançado: '{estado_atual_lido}' não é um estado final.")
        
        print("Caminho até agora:", " -> ".join(estados_percorridos)) #caminho percorrido até o momento

print("Obrigado por utilizar o conversor e validador de autômatos não determinísticos do Keven")

