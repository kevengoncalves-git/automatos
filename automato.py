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

"""alfabeto = input("Insira o alfabeto do seu autômato(separe os simbolos por vírgula): ")
lista_simbolos = tuple(organizar_entrada(alfabeto))

print(f"Seu alfabeto é: {lista_simbolos}\n")

estados = input("Insira os estados do seu autômato(separe os estados por vírgula): ")
lista_estados = tuple(organizar_entrada(estados))

print(f"Seus estados são: {lista_estados}\n")
print()

estados_finais = input("Insira os estados finais do seu autômato(separe os estados por vírgula): ")
lista_estados_finais = tuple(organizar_entrada(estados_finais))

print(f"Seus estados finais são: {lista_estados_finais}\n")"""

estado_inicial = 'q0'

#teste com AFND predefinido
funcao_transicao = {}
funcao_transicao = {'q0': {'0': ['q1', 'q2', 'q5'], '1': []}, 'q1': {'0': [], '1': ['q3']}, 'q2': {'0': [], '1': ['q4']}, 'q3': {'0': ['q5', 'q6'], '1': []}, 'q4': {'0': ['q5', 'q6'], '1': []}, 'q5': {'0': [], '1': ['q3', 'q4']}, 'q6': {'0': ['q6'], '1': ['q6']}}
lista_simbolos = ('0', '1')
lista_estados = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6')
lista_estados_finais = ('q5', 'q6')

#Cria a estrutura inicial da função de transição
"""for estado in sorted(lista_estados):
    funcao_transicao[estado] = { #estado como chave principal
        simbolo: list() for simbolo in sorted(lista_simbolos) #simbolos como chaves secundárias : valores vazios (listas)   
    }"""

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

""" for estado in lista_estados:
    inserir_transicao(estado) """

print("Função de transição final do AFND:")
for estado, simbolo in funcao_transicao.items():
    print(f"Estado: {estado}")
    for chave, destinos in simbolo.items():
        print(f"Símbolo: {chave} | Destinos: {destinos}")
    print("-"*30)

def percorre_afnd(estado_atual, palavra, cabeca_de_leitura, caminho):
    if cabeca_de_leitura == len(palavra): #caso onde a cabeça de leitura alcança o final da palavra
        print("Caminho:", " -> ".join(caminho)) #printa o caminho percorrido
        if estado_atual in lista_estados_finais:
            print(f"A palavra '{palavra}' é aceita pelo AFND! Estado final alcançado: '{estado_atual}'\n")
            return True
        else: #se chegar ao final da palavra e o estado atual não for final
            print(f"A palavra '{palavra}' não é aceita neste caminho. Estado final: '{estado_atual}'\n")
            return False

    simbolo = palavra[cabeca_de_leitura] #recolhe um símbolo da palavra

    #teste pra ver se o símbolo é válido
    if simbolo not in lista_simbolos: 
        print(f"Palavra inválida -> O símbolo '{simbolo}' na posição {cabeca_de_leitura} não pertence ao alfabeto do AFND.\n")
        return False

    #caminho bloqueado se o estado atual não tiver transições para o símbolo lido
    #funcao_transicao[estado_atual] -> dicionário de transições do estado atual
    if estado_atual not in funcao_transicao or simbolo not in funcao_transicao[estado_atual]:
        print("Caminho:", " -> ".join(caminho), "(X)")
        return False

    aceita = False
    estados_de_destino = funcao_transicao[estado_atual][simbolo]

    # Explora recursivamente TODOS os estados de destino
    for destino in estados_de_destino:
        aceita = percorre_afnd(
            destino,
            palavra,
            cabeca_de_leitura + 1, #avança a cabeça de leitura 
            caminho + [destino] #atualiza o caminho percorrido
        ) or aceita #se algum caminho aceitar a palavra, aceita será True

    return aceita

while True:
    resposta = input("Deseja verificar uma palavra no AFND? (s/n): ").strip().lower()
    if resposta == 'n':
        break
    if resposta != 's':
        print("Resposta inválida. Digite 's' ou 'n'.\n")
        continue

    print("Iniciando verificação da palavra...\n")
    palavra = input("Insira a palavra a ser verificada pelo AFND: ")
    print("-"*50)
    resultado = percorre_afnd(estado_inicial, palavra, 0, [estado_inicial])

    if resultado:
        print("-"*50)
        print(f"A palavra '{palavra}' é aceita pelo AFND (existe pelo menos um caminho válido).\n")
    else:
        print("-"*50)
        print(f"A palavra '{palavra}' NÃO é aceita pelo AFND.\n")


print("Obrigado por utilizar o conversor e validador de autômatos não determinísticos do Keven")

def criar_funcao_transicao_afd(funcao_afnd, estado_inicial, lista_simbolos):

    funcao_afd = dict()

    # estado inicial do AFD é um conjunto
    estado_inicial_afd = frozenset({estado_inicial})

    estados_em_processamento = [estado_inicial_afd]
    estados_processados = set()

    funcao_afd[estado_inicial_afd] = dict()

    while estados_em_processamento:
        estado_atual = estados_em_processamento.pop(0) #estado_atual -> conjunto de estados

        if estado_atual in estados_processados: #se o estado já foi processado -> passa pro próximo
            continue

        estados_processados.add(estado_atual) #adiciona o estado atual aos processados
        funcao_afd.setdefault(estado_atual, dict()) #estado atual como chave de um dicionario 
        #'setdefault' cria a chave se não existir

        for simbolo in lista_simbolos: #pega os símbolos do AFND

            novos_destinos = set()

            for estado in estado_atual:
                if simbolo in funcao_afnd.get(estado, {}): # testa se tem alguma transição pro símbolo
                    novos_destinos.update(funcao_afnd[estado][simbolo]) #update pra adicionar os estados e não uma lista de estados

            novo_estado = frozenset(novos_destinos)

            funcao_afd[estado_atual][simbolo] = novo_estado

            if novo_estado not in estados_processados:
                estados_em_processamento.append(novo_estado)

    return funcao_afd

funcao_transicao_afd = criar_funcao_transicao_afd(funcao_transicao, estado_inicial, lista_simbolos)
#remoção dos estados vazios (-) do dicionario
funcao_transicao_afd = {item_valido: valor for item_valido, valor in funcao_transicao_afd.items() if item_valido}

#função pra poupar meu esforço de organizar o print dos estados
def imprimir_nomes_estados(funcao_transicao):
    for estado, transicoes in funcao_transicao.items():
        estado_formatado = ", ".join(sorted(estado)) if estado else "-"
        print(f"Estado: {{{estado_formatado}}}")
        for simbolo, destinos in transicoes.items():
            destinos_formatados = ", ".join(sorted(destinos)) if destinos else "-"
            print(f"  com símbolo '{simbolo}' -> {{{destinos_formatados}}}")
        print("-" * 50)

print("-"*50)
print("\nFunção de Transição do AFD antes da modificação dos nomes:\n")
#estado com nomes originais
imprimir_nomes_estados(funcao_transicao_afd)

#função afd com nomes modificados 'P0', 'P1', ...
nova_funcao_transicao_afd = {f"P{i}": valor for i, valor in enumerate(funcao_transicao_afd.values())}
#valor -> valores nas chaves do afd original

#criação de uma lista de referência entre os estados originais e os novos
lista_referencia_estados = dict()

for estado_original, estado_novo in zip(funcao_transicao_afd.keys(), nova_funcao_transicao_afd.keys()):
    lista_referencia_estados[estado_original] = estado_novo

#verificação dos novos estados finais do AFD
estados_finais_novos = set()
for referencia in lista_referencia_estados.keys():
    for estado_final in lista_estados_finais:
        if estado_final in referencia:
            estados_finais_novos.add(lista_referencia_estados[referencia])

print("-"*50)
print("Lista de referência de estados (original -> novo):")
for nome_original, novo_nome in lista_referencia_estados.items():
    print(f"Estado original: {set(nome_original)} -> Novo nome: {novo_nome}")
print("-"*50)


for estado, transicoes in nova_funcao_transicao_afd.items():
    for simbolo, destinos in transicoes.items():
        if destinos in lista_referencia_estados:
            nova_funcao_transicao_afd[estado][simbolo] = lista_referencia_estados[destinos]
            #lista_referencia_estados[destinos] -> pega o novo nome do estado de destino
        
print("-"*50)
print(f"Estados finais do AFD : {sorted(estados_finais_novos)}\n")
print(f"AFD APÓS a modificação de nomes:")
for estado, transicoes in nova_funcao_transicao_afd.items():
    print(f"Estado: {estado}")
    for simbolo, destino in transicoes.items():
        print(f"  com símbolo '{simbolo}' -> {destino}") if destino else print(f"  com símbolo '{simbolo}' -> -")
    print("-" * 50)
print("-"*50)

