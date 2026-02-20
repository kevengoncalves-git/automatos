from tabulate import tabulate
import pandas as pd

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
    print("-"*50)
    print("Verificando se há transições vazias\n")
    tem_transicoes_vazias = False
    for estado, transicoes in funcao_transicao_afd.items():
        for simbolo, destino in transicoes.items():
            if isinstance(destino, frozenset): #Se destino for um frozenset significa que está vazio
                funcao_transicao_afd[estado][simbolo] = "A"
                tem_transicoes_vazias = True
    if tem_transicoes_vazias: #Inserção do estado artificial
        print("Há transições vazias")
        funcao_transicao_afd["A"] = {simbolo: "A" for simbolo in lista_simbolos}

    return funcao_transicao_afd      

#Tabela de pares para minimização
def imprimir_tabela_de_pares(funcao_transicao_afd):
    estados = [estado for estado in funcao_transicao_afd.keys()]

    #Colunas: primeiro ao penúltimo
    colunas = estados[:-1]

    tabela = []

    #Linhas: segundo ao último
    for i in range(1, len(estados)):
        linha = [estados[i]]
        for j in range(len(estados) - 1):
            if j >= i:
                linha.append("-")
            else:
                linha.append("")
        tabela.append(linha)

    cabecalho = [""] + colunas

    print(tabulate(tabela, headers=cabecalho, tablefmt="grid"))
    print("-"*50)

#Marca os pares trivialmente equivalentes (finais e não finais)
def marcar_pares_trivialmente_equivalentes(funcao_transicao_afd, estados_finais):
    estados = list(funcao_transicao_afd.keys())
    print(f"Estados finais: {sorted(estados_finais)} | Estados: {estados}\n")

    dataframe_pares = pd.DataFrame(
        index=estados[1:],     # linhas: do segundo ao último
        columns=estados[:-1]   # colunas: do primeiro ao penúltimo
    )

    for i in range(1, len(estados)):
        for j in range(len(estados) - 1):
            if j >= i:
                dataframe_pares.iat[i-1, j] = "-"
            else:
                estado1 = estados[i]  # linha
                estado2 = estados[j]  # coluna

                if (estado1 in estados_finais) != (estado2 in estados_finais):
                    dataframe_pares.iat[i-1, j] = "x"
                else:
                    dataframe_pares.iat[i-1, j] = ""

    # Impressão com tabulate
    print(
        tabulate(
            dataframe_pares.values,
            headers=dataframe_pares.columns,
            showindex=list(dataframe_pares.index),
            tablefmt="grid"
        )
    )

    return dataframe_pares

#Printa todas as regras gramaticais dos estados nao terminais
def printar_regras_gramaticais(regras_gramaticais_P):
    for estado_nao_terminal, regras in regras_gramaticais_P.items():
        print(f"Estado não Terminal: {estado_nao_terminal}")
        for regra in regras:
            if regra == '-':
                print(f"Regra: {estado_nao_terminal} -> ε (transição vazia)")
            else:
                print(f"Regra: {estado_nao_terminal} -> {regra}")

#Verifica se a gramática é linear ou não
def verificar_tipo_gramatica(regras_gramaticais_P):
    print("-"*50)
    print("Verificação se a gramática é GL ou GLC:")
    for regras in regras_gramaticais_P.values():
        e_gramatica_linear = False
        for regra in regras:
            if regra == '-':
                continue
            else:
                regra_str = str(regra)
                cont = 0
                for char in regra_str:
                    if char.isupper():
                        cont += 1
                if cont > 1:
                   print(f"Regra: {regra_str} prova que é uma GLC")
                   break
                else: 
                    e_gramatica_linear = True
                cont = 0
    if e_gramatica_linear:
        print("\n Resultado: Gramática Linear)")
    else:
        print("\nResultado: Gramática Não Linear (GLC)")
    print("-"*50)

#Marca os pares não equivalentes
def marcar_pares_nao_equivalentes(tabela_minimizacao, nova_funcao_transicao_afd, lista_simbolos):
    print("-"*50)
    print("Marcando pares não equivalentes com ⦻")

    estados = list(nova_funcao_transicao_afd.keys())
    linhas = estados[1:]
    #colunas = estados[:-1]

    print("Pares vazios (linha|coluna):")

    houve_mudancas = True #verifica se algum par foi marcado durante a iteração

    while houve_mudancas:
        houve_mudancas = False #por enquanto sem mudanças

        for coluna in tabela_minimizacao.columns:
            for linha in linhas:
                if tabela_minimizacao.at[linha, coluna] == "":

                    print(f"Verificando célula: {linha}{coluna}")

                    for simbolo in lista_simbolos:

                        transicao_linha = nova_funcao_transicao_afd[linha][simbolo]
                        transicao_coluna = nova_funcao_transicao_afd[coluna][simbolo]

                        print(f"Transição ao ler '{simbolo}': {transicao_linha}{transicao_coluna}")

                        # ---------------------------------------------
                        # 🔥 MODIFICAÇÃO 1: Ignorar apenas AA
                        # ---------------------------------------------
                        if transicao_linha == transicao_coluna:
                            continue

                        # ---------------------------------------------
                        # 🔥 MODIFICAÇÃO 2: Verificar se ambos existem
                        # na lista de estados antes de continuar
                        # ---------------------------------------------
                        if transicao_linha not in estados or transicao_coluna not in estados:
                            continue

                        # ---------------------------------------------
                        # 🔥 MODIFICAÇÃO 3 (PRINCIPAL):
                        # NORMALIZAÇÃO DO PAR
                        # Garante que P4A = AP4
                        # Sempre coloca o maior índice como linha
                        # e o menor como coluna
                        # ---------------------------------------------
                        idx1 = estados.index(transicao_linha)
                        idx2 = estados.index(transicao_coluna)

                        if idx1 > idx2:
                            linha_norm = transicao_linha
                            coluna_norm = transicao_coluna
                        else:
                            linha_norm = transicao_coluna
                            coluna_norm = transicao_linha

                        print(f"Par normalizado: {linha_norm}{coluna_norm}")

                        # ---------------------------------------------
                        # 🔥 MODIFICAÇÃO 4:
                        # Só consulta a tabela DEPOIS da normalização
                        # ---------------------------------------------
                        if (
                            linha_norm in tabela_minimizacao.index and
                            coluna_norm in tabela_minimizacao.columns
                        ):
                            if tabela_minimizacao.at[linha_norm, coluna_norm] == 'x' or tabela_minimizacao.at[linha_norm, coluna_norm] == '⦻':
                                tabela_minimizacao.at[linha, coluna] = '⦻'
                                houve_mudancas = True #se marcou é pq teve mudança
                                print(f"Par {linha_norm}{coluna_norm} já marcado.")
                                print(f"Marcando {linha}{coluna} como não equivalente.\n")
                                break

                    print("\n" + "-"*50)
                    print("Atualização da tabela de minimização:")
                    print(
                        tabulate(
                            tabela_minimizacao.values,
                            headers=tabela_minimizacao.columns,
                            showindex=list(tabela_minimizacao.index),
                            tablefmt="grid"
                        )
                    )
                    print("\n")


    print(tabela_minimizacao)
    return tabela_minimizacao

#teste com AFND pré-definido
estado_inicial = 'q0'
funcao_transicao = {}
funcao_transicao = {'q0': {'0': ['q1', 'q2', 'q5'], '1': []}, 'q1': {'0': [], '1': ['q3']}, 'q2': {'0': [], '1': ['q4']}, 'q3': {'0': ['q5', 'q6'], '1': []}, 'q4': {'0': ['q5', 'q6'], '1': []}, 'q5': {'0': [], '1': ['q3', 'q4']}, 'q6': {'0': ['q6'], '1': ['q6']}}
lista_simbolos = ('0', '1')
lista_estados = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6')
lista_estados_finais = ('q5', 'q6')

#teste com gramática pré-definida
estados_nao_terminais = ('S', 'A', 'B', 'C')
estados_terminais = ('a', 'b')
regras_gramaticais_P = {'S': ["aA", "bS"], 'A': ["aB", "bS"], 'B': ["aC", "bS"], 'C': ["AaC", "bC", '-']} #'-' transição vazia
simbolo_inicial = 'S'

printar_regras_gramaticais(regras_gramaticais_P)
verificar_tipo_gramatica(regras_gramaticais_P)

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
print("-"*50)
print("Preparação para a minimização do afd")
nova_funcao_transicao_afd = preencher_transicoes_vazias_afd(nova_funcao_transicao_afd)

#Print do preenchimento com estados vazios
printar_tabela_funcao_transicao(nova_funcao_transicao_afd, lista_simbolos)

#Print da tabela de pares
imprimir_tabela_de_pares(nova_funcao_transicao_afd)

#Marcando com x os pares trivialmente equivalentes(finais e não finais)
tabela_minimizacao = marcar_pares_trivialmente_equivalentes(nova_funcao_transicao_afd, estados_finais_novos)

#Tabela de pares atualizada após marcar os pares trivialmente equivalentes            
tabela_minimizacao_atualizada = marcar_pares_nao_equivalentes(tabela_minimizacao, nova_funcao_transicao_afd, lista_simbolos)

