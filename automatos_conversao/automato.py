from tabulate import tabulate
import pandas as pd
from menu_automato import menu, menu_secundario

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

#Cria uma função de transição vazia pro AFND ou AFD
def inicializar_funcao_transicao(lista_estados, lista_simbolos, tipo_automato):
    funcao = {}

    for estado in lista_estados:

        funcao[estado] = {}

        for simbolo in lista_simbolos:

            if tipo_automato == "AFD":
                funcao[estado][simbolo] = None
            else:  # AFND
                funcao[estado][simbolo] = []

    return funcao

def inserir_transicao(funcao_transicao, estado_atual, tipo_automato):
    for simbolo in funcao_transicao[estado_atual]:
        print("-"*50)
        print(f"--> Trabalhando com o estado {estado_atual}")
        entrada = input(f"Destino(s) para '{estado_atual}' com símbolo '{simbolo}': ").strip()
        print("-"*50)

        #se o cara apertar enter sem digitar nada --> caso vazio
        if entrada == "":
            if tipo_automato == "AFD":
                funcao_transicao[estado_atual][simbolo] = "-"
            else:
                funcao_transicao[estado_atual][simbolo] = ["-"]
            continue

        destinos = entrada.split(",")
        destinos_processados = []

        for destino in destinos:
            destino = destino.strip()

            if destino in lista_estados:
                destinos_processados.append(destino)
            else:
                print(f"Estado '{destino}' inválido e será ignorado.")

        if tipo_automato == "AFD":

            if len(destinos_processados) > 1:
                print("AFD não pode ter vários destinos")
                destinos_processados = destinos_processados[:1]

            funcao_transicao[estado_atual][simbolo] = destinos_processados[0]

        else:
            funcao_transicao[estado_atual][simbolo] = destinos_processados

#função recursiva para percorrer o AFND e verificar se a palavra é aceita
def percorre_afnd(estado_atual, palavra, cabeca_de_leitura, caminho):
    if cabeca_de_leitura == len(palavra): #caso onde a cabeça de leitura alcança o final da palavra
        print("Caminho:", " -> ".join(caminho)) #printa o caminho percorrido
        if estado_atual in estados_finais:
            print(f"A palavra '{palavra}' é aceita pelo AFND! Estado final alcançado: '{estado_atual}'\n")
            return True
        else: #se chegar ao final da palavra e o estado atual não for final
            print(f"A palavra '{palavra}' não é aceita neste caminho. Estado final: '{estado_atual}'\n")
            return False

    simbolo = palavra[cabeca_de_leitura] #recolhe um símbolo da palavra

    #teste pra ver se o símbolo é válido
    if simbolo not in lista_simbolos: 
        print(f"Palavra inválida -> O símbolo '{simbolo}' na posição {cabeca_de_leitura} da cabeça de leitura não pertence ao alfabeto do AFND.\n")
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
        if aceita:
            break #se já aceitou, não precisa continuar explorando outros destinos
    return aceita

#tradução do afnd em afd
def criar_funcao_transicao_afd(funcao_afnd, estado_inicial, lista_simbolos):

    funcao_afd = dict()
    estado_inicial_afd = frozenset({estado_inicial})

    estados_em_processamento = [estado_inicial_afd]
    estados_processados = set()

    while estados_em_processamento:
        estado_atual = estados_em_processamento.pop(0)

        if estado_atual in estados_processados:
            continue

        estados_processados.add(estado_atual)
        funcao_afd.setdefault(estado_atual, dict())

        for simbolo in lista_simbolos:

            novos_destinos = set()

            for estado in estado_atual:
                transicoes = funcao_afnd.get(estado, {}).get(simbolo, [])
                
                #verifica se o destino não é vazio ou um estado inválido
                for destino in transicoes:
                    if destino and destino != "-":
                        novos_destinos.add(destino)

            if novos_destinos:
                novo_estado = frozenset(novos_destinos)
                funcao_afd[estado_atual][simbolo] = novo_estado

                if novo_estado not in estados_processados:
                    estados_em_processamento.append(novo_estado)
            else:
                funcao_afd[estado_atual][simbolo] = None

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
def percorre_afd(estado_atual, palavra, lista_simbolos, estados_finais, funcao_transicao):
    caminho = [estado_atual]  # lista para armazenar o caminho percorrido começando pelo P0
    print(f"Caminho: {estado_atual}")
    for cabeca_de_leitura in range(len(palavra)):
        simbolo = palavra[cabeca_de_leitura]

        if simbolo not in lista_simbolos:
            print("Símbolo da palavra inválido")
            return False

        estado_atual = funcao_transicao.get(estado_atual, {}).get(simbolo)
        caminho.append(estado_atual) if estado_atual else caminho.append("X")

        print(f"Caminho: {' -> '.join(map(str, caminho))}")

    # verificação final de aceitação
    if estado_atual in estados_finais:
        return True
    else:
        print(f"Estado alcançado: {estado_atual}")
        return False

#recolhedor de palavras para teste no afnd e afd
def recolher_palavra(tipo, estados_finais):
    while True:
        print("Iniciando verificação da palavra...\n")
        palavra = input(f"Insira a palavra a ser verificada pelo {tipo}: ")
        print("-"*50)
        if tipo == "AFND":
            resultado = percorre_afnd('q0', palavra, 0, [estado_inicial])
        else:
            resultado = percorre_afd('P0', palavra, lista_simbolos, estados_finais, funcao_transicao)
        #resultado = percorre_afd('P0', palavra, lista_simbolos, estados_finais_novos)

        if resultado:
            print("-"*50)
            print(f"A palavra '{palavra}' é aceita pelo {tipo} (existe pelo menos um caminho válido).\n")
            print(f"Conjunto de estados finais do {tipo}: {sorted(estados_finais)}\n")
        else:
            print("-"*50)
            print(f"A palavra '{palavra}' NÃO é aceita pelo {tipo}.\n")
            print(f"Conjunto de estados finais do {tipo}: {sorted(estados_finais)}\n")
        print("-"*50)

        resposta = input(f"Deseja verificar outra palavra no {tipo}? (s/n): ").strip().lower()
        if resposta == 'n':
            print("Até logo parceiro :)\n")
            break
        if resposta != 's':
            while resposta not in ['s', 'n']:
                resposta = input("Resposta inválida. Digite 's' para sim ou 'n' para não: ").strip().lower()

#Verificando se o automato é deterministico ou não
def verificar_se_eh_afd(funcao_transicao, lista_simbolos):
    for estado, transicoes in funcao_transicao.items():
        for simbolo in lista_simbolos:
            # Verifica se o símbolo existe no estado
            if simbolo not in transicoes:
                print(f"Estado {estado} não possui transição pro símbolo '{simbolo}'")
                return False
            destino = transicoes[simbolo]
            # Se for lista é AFND
            if isinstance(destino, list):
                if len(destino) > 1:
                    print(f"Não determinismo detectado em ({estado}, {simbolo}) → {destino}")
                    return False

    print("O autômato é determinístico (AFD válido)")
    return True

#Preenche quando possível transições vazias do afd
def preencher_transicoes_vazias_afd(funcao_transicao_afd):
    print("-"*50)
    print("Verificando se há transições vazias\n")
    tem_transicoes_vazias = False
    for estado, transicoes in funcao_transicao_afd.items():
        for simbolo, destino in transicoes.items():
            if destino is None: #Se destino for None significa que está vazio
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
def marcar_pares_trivialmente_nao_equivalentes(funcao_transicao_afd, estados_finais):
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

#Marca os pares não equivalentes
def marcar_pares_nao_equivalentes(tabela_minimizacao, funcao_transicao_afd_espacos_vazios, lista_simbolos):
    print("-"*50)
    print("Marcando pares não equivalentes com ⦻")

    estados = list(funcao_transicao_afd_espacos_vazios.keys())
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
                        transicao_linha = funcao_transicao_afd_espacos_vazios[linha][simbolo]
                        transicao_coluna = funcao_transicao_afd_espacos_vazios[coluna][simbolo]
                        print(f"Transição ao ler '{simbolo}': {transicao_linha}{transicao_coluna}")

                        # Ignorando apenas AA
                        if transicao_linha == transicao_coluna:
                            continue

                        #Verificando se existem na lista de estados antes de continuar
                        if transicao_linha not in estados or transicao_coluna not in estados:
                            continue

                        # Normalizações de cada pa
                        # Por ex: P4A = AP4
                        # Sempre coloca o maior índice como linha e o menor como coluna
                        # linha = 1, len(estados) e coluna = 0, len(estados)-1
                        idx1 = estados.index(transicao_linha)
                        idx2 = estados.index(transicao_coluna)

                        if idx1 > idx2:
                            linha_norm = transicao_linha
                            coluna_norm = transicao_coluna
                        else:
                            linha_norm = transicao_coluna
                            coluna_norm = transicao_linha

                        print(f"Par normalizado: {linha_norm}{coluna_norm}")


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

#Juntar pares equivalentes
def juntar_pares_equivalentes(tabela_minimizacao_atualizada, funcao_transicao_afd):
    print("-"*50)
    estados_equivalentes = set()
    for coluna in tabela_minimizacao_atualizada.columns:
        for linha in tabela_minimizacao_atualizada.index:
            if tabela_minimizacao_atualizada.at[linha, coluna] == "":
                print(f"Par equivalente encontrado: {linha} | {coluna}")
                estados_equivalentes.add(linha)
                estados_equivalentes.add(coluna)

    print("\nEstados equivalentes: ", sorted(estados_equivalentes))

    #junção dos estados em um só
    novo_estado = str()
    for estado in sorted(estados_equivalentes):
        novo_estado += estado

    print("Novo estado após junção dos equivalentes: ", novo_estado)

    #Atualização da função transicao
    for estado, transicoes in funcao_transicao_afd.items():
        for simbolo, destino in transicoes.items():
            if destino in estados_equivalentes:
                funcao_transicao_afd[estado][simbolo] = novo_estado
                   

    afd_minimizado = dict()
    for estado, transicoes in funcao_transicao_afd.items():
        if estado not in estados_equivalentes:
            afd_minimizado[estado] = transicoes
            
    #next e iter pra pegar a próxima chave do dicionário
    afd_minimizado[novo_estado] = funcao_transicao_afd[next(iter(estados_equivalentes))]
    for estado, transicoes in afd_minimizado.items():
        for simbolo, destino in transicoes.items():
            if destino == "A":
                afd_minimizado[estado][simbolo] = "-"
    
    #Dropando a linha com A
    if "A" in afd_minimizado:
        del afd_minimizado["A"]
        
    estados_finais_novos = set()
    for estado in afd_minimizado.keys():
        for estado_final in estados_finais:
            if estado_final in estado:
                estados_finais_novos.add(estado)

    print("-"*50)
    print("AFD após junção dos equivalentes:")
    formalizar_automato(lista_simbolos, list(afd_minimizado.keys()), "Min AFD", "P0", sorted(list(estados_finais_novos)))
    printar_formalizacao(formalizar_automato(lista_simbolos, list(afd_minimizado.keys()), "Min AFD", "P0", sorted(list(estados_finais_novos))))
    return afd_minimizado, estados_finais_novos


#---------------------------------Chamadas de Função---------------------------------
#teste com AFND pré-definido
estado_inicial = 'q0'
funcao_transicao = {}
funcao_transicao = {'q0': {'0': ['q1', 'q2', 'q5'], '1': []}, 'q1': {'0': [], '1': ['q3']}, 'q2': {'0': [], '1': ['q4']}, 'q3': {'0': ['q5', 'q6'], '1': []}, 'q4': {'0': ['q5', 'q6'], '1': []}, 'q5': {'0': [], '1': ['q3', 'q4']}, 'q6': {'0': ['q6'], '1': ['q6']}}
lista_simbolos = ('0', '1')
lista_estados = ('q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6')
estados_finais = ('q5', 'q6')
while True:
    opcao = menu()

    #===================INSERINDO INFO DO AFND OU AFD MANUALMENTE===================
    if opcao in [1, 2]:
        #entrada do usuário para criar o AFND ou AFD manual
        alfabeto = input("Insira o alfabeto do seu autômato(separe os simbolos por vírgula): ")
        lista_simbolos = tuple(organizar_entrada(alfabeto))

        print(f"Seu alfabeto é: {lista_simbolos}\n")

        estados = input("Insira os estados do seu autômato(separe os estados por vírgula): ")
        lista_estados = tuple(organizar_entrada(estados))

        print(f"Seus estados são: {lista_estados}\n")
        print()

        estados_finais = input("Insira os estados finais do seu autômato(separe os estados por vírgula): ")
        estados_finais = tuple(organizar_entrada(estados_finais))

        print(f"Seus estados finais são: {estados_finais}\n")

        tipo_automato = input("Digite o tipo do seu autômato (AFD ou AFND): ").strip().upper()
        while tipo_automato not in ["AFD", "AFND"]:
            print("Tipo de autômato inválido. Digite 'AFD' ou 'AFND'.")
            tipo_automato = input("Digite o tipo do seu autômato (AFD ou AFND): ").strip().upper()

        tupla_formalizacao_afnd = formalizar_automato(lista_simbolos, 
                                                      lista_estados, 
                                                      f"{tipo_automato}", 
                                                      estado_inicial, 
                                                      estados_finais)
        
        funcao_transicao = inicializar_funcao_transicao(lista_estados, lista_simbolos, tipo_automato)

        for estado in lista_estados:
            inserir_transicao(funcao_transicao, estado, tipo_automato)

        formalizacao = formalizar_automato(lista_simbolos, lista_estados, f"{tipo_automato}", estado_inicial, estados_finais)
        printar_formalizacao(formalizacao)
        print(f"Função de transição do {tipo_automato}:")
        printar_tabela_funcao_transicao(funcao_transicao, lista_simbolos)

        while True:
            opcao_secundaria = menu_secundario()

            if opcao_secundaria == 1 and tipo_automato == "AFND":
                recolher_palavra("AFND", estados_finais)
            elif opcao_secundaria == 1 and tipo_automato == "AFD":
                recolher_palavra("AFD", estados_finais)
            elif opcao_secundaria == 2:
                break
            else:
                exit()



    #===================AFND PRÉ-DEFINIDO PRA TESTE DO USUARIO===================
    elif opcao == 5:
        print("-"*50)
        print("Prossegindo com o AFND pré-definido...")
        tupla_formalizacao_afnd = formalizar_automato(lista_simbolos, 
                                                      lista_estados, 
                                                      "AFND", 
                                                      estado_inicial, 
                                                      estados_finais)
        printar_formalizacao(tupla_formalizacao_afnd)
        print("-"*50)

        #FORMALIZAÇÃO DO AFND
        print("Função de transição do AFND:")
        printar_tabela_funcao_transicao(funcao_transicao, lista_simbolos)

        while True:
            opcao_secundaria = menu_secundario()

            if opcao_secundaria == 1:
                recolher_palavra("AFND", estados_finais)
            elif opcao_secundaria == 2:
                break
            else:
                exit()
    #===================CONVERSÃO DO AFND PRO AFD===================
    elif opcao == 3:
        #função transição do afd apartir do afnd
        print("-"*50)
        print("Iniciando conversão de AFND para AFD...")
        funcao_transicao_afd = criar_funcao_transicao_afd(funcao_transicao, estado_inicial, lista_simbolos)
        #remoção dos estados vazios (-) do dicionario
        funcao_transicao_afd = {item_valido: valor for item_valido, valor in funcao_transicao_afd.items() if item_valido}

        print("-"*50)
        print("\nFunção de Transição do AFD antes da modificação dos nomes:")
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
            for estado_final in estados_finais:
                if estado_final in referencia:
                    estados_finais_novos.add(lista_referencia_estados[referencia])
        estados_finais = estados_finais_novos
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
        tupla_formalizacao_afd = formalizar_automato(lista_simbolos, list(nova_funcao_transicao_afd.keys()), "AFD", "P0", sorted(list(estados_finais)))
        printar_formalizacao(tupla_formalizacao_afd)
        printar_tabela_funcao_transicao(nova_funcao_transicao_afd, lista_simbolos)

        #pegando afd antes da adição das transições artificiais
        funcao_transicao_afd = nova_funcao_transicao_afd.copy()
        funcao_transicao = funcao_transicao_afd

        while True:
            opcao_secundaria = menu_secundario()

            if opcao_secundaria == 1:
                recolher_palavra("AFD", estados_finais)
            elif opcao_secundaria == 2:
                break
            else:
                exit()

    #===================MINIMIZAÇÃO===================
    elif opcao == 4:
        #Preenchimento da nova_função do afd com transições artificiais (quando possível) 
        print("-"*50)
        print("Verificando se há mais de duas transições para um símbolo")

        if not verificar_se_eh_afd(funcao_transicao, lista_simbolos):
            print("Erro: o autômato não é determinístico")
        
        else:
            print(funcao_transicao)
            print("Preparação para a minimização do afd")

            funcao_transicao_afd_espacos_vazios = preencher_transicoes_vazias_afd(funcao_transicao)

            #Print do preenchimento com estados vazios
            printar_tabela_funcao_transicao(funcao_transicao_afd_espacos_vazios, lista_simbolos)

            #Print da tabela de pares
            imprimir_tabela_de_pares(funcao_transicao_afd_espacos_vazios)

            #Marcando com x os pares trivialmente não equivalentes(finais e não finais)
            tabela_minimizacao = marcar_pares_trivialmente_nao_equivalentes(funcao_transicao_afd_espacos_vazios, estados_finais)

            #Tabela de pares atualizada após marcar os pares não equivalentes            
            tabela_minimizacao_atualizada = marcar_pares_nao_equivalentes(tabela_minimizacao, funcao_transicao_afd_espacos_vazios, lista_simbolos)

            #Junção dos pares equivalente e criação do AFD minimizado
            tupla_resultados = juntar_pares_equivalentes(tabela_minimizacao_atualizada, funcao_transicao)
            afd_minimizado = tupla_resultados[0]
            estados_finais = tupla_resultados[1]

            print("-"*50)
            print("AFD Minimizado:")
            printar_tabela_funcao_transicao(afd_minimizado, lista_simbolos)

            while True:
                opcao_secundaria = menu_secundario()

                if opcao_secundaria == 1:
                    recolher_palavra("AFD Minimizado", estados_finais)
                elif opcao_secundaria == 2:
                    break
                else:
                    exit()

    #===================SAÍDA===================
    elif opcao in [3,6]:
        print("Obrigado por usar o conversor e validador de autômatos do Keven, Camille e Erick")
        exit()
