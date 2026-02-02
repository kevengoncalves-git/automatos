from tabulate import tabulate

print("-"*50)
print("Bem vindo ao conversor e validador de autômatos")
print("-"*50)

#pegar inputs do usuário
def organizar_entrada(entrada):
    elementos = entrada.split(",") #retira as vírgulas e cria um conjunto com os elementos
    elementos_processados = list() #cria um conjunto vazio para armazenar os elementos
    for elemento in elementos:
        elemento = elemento.strip()
        elementos_processados.append(elemento)
    return elementos_processados

#função para formalizar o auttomato
def formalizar_automato(alfabeto, estados, tipo, estado_inicial, estados_finais):
    tupla_formalizacao = (alfabeto, estados, tipo, estado_inicial, estados_finais)
    return tupla_formalizacao

#função para printar a formalização do automato de forma mais bonita
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

#função para printar a função de transição do automato em formato de tabela
def printar_tabela_funcao_transicao(funcao_transicao, lista_simbolos):
    tabela = []
    for estado, transicoes in funcao_transicao.items():
        linha = [estado]
        for simbolo in lista_simbolos:
            destinos = transicoes.get(simbolo, [])
            if isinstance(destinos, list):
                destinos = ", ".join(destinos) if destinos else "-"
            else :
                destinos = destinos if destinos else "-"
            linha.append(destinos)
        tabela.append(linha)
    headers = ["Estado"] + list(lista_simbolos)
    print(tabulate(tabela, headers=headers, tablefmt="grid", stralign="center"))

#função para inserir transições no afnd
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

#função recursiva para percorrer o AFND e verificar se a palavra é aceita
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

#tradução do afnd em afd
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

#função pra poupar meu esforço de organizar o print dos estados do afd antigo
def imprimir_tabela_nomes_estados(funcao_transicao, lista_simbolos):
    tabela = []
    for estado, transicoes in funcao_transicao.items():
        estado_formatado = f"<{''.join(sorted(estado))}>" if estado else '-'
        linha = [estado_formatado]
        for simbolo in lista_simbolos:
            destinos = transicoes.get(simbolo, frozenset())
            destinos_formatados = f"<{''.join(sorted(destinos))}>" if destinos else '-'
            linha.append(destinos_formatados)
        tabela.append(linha)
    headers = ["Estado"] + list(lista_simbolos)
    print(tabulate(tabela, headers=headers, tablefmt="grid", stralign="center"))

#função para percorrer o AFD e verificar se a palavra é aceita
def percorre_afd(estado_atual, palavra, lista_simbolos, lista_estados_finais):
    caminho = [estado_atual]  # lista para armazenar o caminho percorrido começando pelo P0
    print(f"Caminho: {estado_atual}")
    for cabeca_de_leitura in range(len(palavra)):
        simbolo = palavra[cabeca_de_leitura]

        if simbolo not in lista_simbolos:
            print("Símbolo da palavra inválido")
            return False

        estado_atual = nova_funcao_transicao_afd.get(estado_atual, {}).get(simbolo)
        caminho.append(estado_atual) if estado_atual else caminho.append("X")

        print(f"Caminho: {' -> '.join(map(str, caminho))}")

    # verificação final de aceitação
    if estado_atual in lista_estados_finais:
        return True
    else:
        return False

#entrada do usuário para criar o AFND manual
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

#recolhedor de palavras para teste no afnd e afd
def recolher_palavra(tipo, estados_finais):
    while True:
        resposta = input(f"Deseja verificar uma palavra no {tipo}? (s/n): ").strip().lower()
        if resposta == 'n':
            print("Obrigado por utilizar o conversor e validador de palavras do Keven")
            break
        if resposta != 's':
            print("Resposta inválida. Digite 's' ou 'n'.\n")
            continue

        print("Iniciando verificação da palavra...\n")
        palavra = input(f"Insira a palavra a ser verificada pelo {tipo}: ")
        print("-"*50)
        if tipo == "AFND":
            resultado = percorre_afnd('q0', palavra, 0, [estado_inicial])
        else:
            resultado = percorre_afd('P0', palavra, lista_simbolos, estados_finais)
        #resultado = percorre_afd('P0', palavra, lista_simbolos, estados_finais_novos)

        if resultado:
            print("-"*50)
            print(f"A palavra '{palavra}' é aceita pelo {tipo} (existe pelo menos um caminho válido).\n")
            print(f"Conjunto de estados finais do {tipo}: {sorted(estados_finais)}\n")
        else:
            print("-"*50)
            print(f"A palavra '{palavra}' NÃO é aceita pelo {tipo}.\n")
            print(f"Conjunto de estados finais do {tipo}: {sorted(estados_finais)}\n")

#Preenche quando possível transições vazias do afd
def preencher_transicoes_vazias_afd(funcao_transicao_afd):
    tem_transicoes_vazias = False
    for estado, transicoes in funcao_transicao_afd.items():
        for simbolo, destino in transicoes.items():
            if isinstance(destino, frozenset): #Se destino for um frozenset significa que está vazio
                funcao_transicao_afd[estado][simbolo] = "A"
                tem_transicoes_vazias = True
    if tem_transicoes_vazias: #Inserção do estado artificial
        funcao_transicao_afd["A"] = {simbolo: "A" for simbolo in lista_simbolos}

    return funcao_transicao_afd      
#teste com AFND predefinido
estado_inicial = 'q0'
funcao_transicao = {}
funcao_transicao = {'q0': {'0': ['q1', 'q2', 'q5'], '1': []}, 'q1': {'0': [], '1': ['q3']}, 'q2': {'0': [], '1': ['q4']}, 'q3': {'0': ['q5', 'q6'], '1': []}, 'q4': {'0': ['q5', 'q6'], '1': []}, 'q5': {'0': [], '1': ['q3', 'q4']}, 'q6': {'0': ['q6'], '1': ['q6']}}
lista_simbolos = ('0', '1')
lista_estados = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6')
lista_estados_finais = ('q5', 'q6')

#formalização do afnd
print("-"*50)
print("Vamos formalizar o seu AFND")
tupla_formalizacao_afnd = formalizar_automato(lista_simbolos, lista_estados, "AFND", estado_inicial, lista_estados_finais)
printar_formalizacao(tupla_formalizacao_afnd)
print("-"*50)

#formalização da função de transição do afnd
print("Função de transição final do AFND:\n")
printar_tabela_funcao_transicao(funcao_transicao, lista_simbolos)

#teste das palavras no afnd
recolher_palavra("AFND", lista_estados_finais)

#função transição do afd apartir do afnd
funcao_transicao_afd = criar_funcao_transicao_afd(funcao_transicao, estado_inicial, lista_simbolos)
#remoção dos estados vazios (-) do dicionario
funcao_transicao_afd = {item_valido: valor for item_valido, valor in funcao_transicao_afd.items() if item_valido}

print("-"*50)
print("\nFunção de Transição do AFD antes da modificação dos nomes:\n")
#estado com nomes originais
imprimir_tabela_nomes_estados(funcao_transicao_afd, lista_simbolos)

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
    nome_original_unido = f"<{''.join(sorted(set(nome_original)))}>"
    print(f"Estado original: {nome_original_unido} -> Novo nome: {novo_nome}")
print("-"*50)

#atualização dos nomes dos estados de destino na função de transição do AFD
for estado, transicoes in nova_funcao_transicao_afd.items():
    for simbolo, destinos in transicoes.items():
        if destinos in lista_referencia_estados:
            nova_funcao_transicao_afd[estado][simbolo] = lista_referencia_estados[destinos]
        
print("-"*50)
print(f"AFD APÓS a modificação de nomes:")
tupla_formalizacao_afd = formalizar_automato(lista_simbolos, list(nova_funcao_transicao_afd.keys()), "AFD", "P0", sorted(list(estados_finais_novos)))
printar_formalizacao(tupla_formalizacao_afd)
printar_tabela_funcao_transicao(nova_funcao_transicao_afd, lista_simbolos)

#testar palavras no afd
recolher_palavra("AFD", estados_finais_novos) 

#Preenchimento da nova_função do afd com transições artificiais (quando possível) 
nova_funcao_transicao_afd = preencher_transicoes_vazias_afd(nova_funcao_transicao_afd)

#Print do preenchimento com estados vazios
printar_tabela_funcao_transicao(nova_funcao_transicao_afd, lista_simbolos)
