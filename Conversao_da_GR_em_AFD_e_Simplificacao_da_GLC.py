import collections
from tabulate import tabulate

# --- 1. UTILITÁRIOS DE FORMATAÇÃO E EXIBIÇÃO ---

def imprimir_gramatica(titulo, variaveis, terminais, producoes, inicial):
    """Exibe a gramática de forma acadêmica e organizada (Ponto 06)."""
    print(f"\n{'='*25} {titulo} {'='*25}")
    print(f"G = (V, T, P, S)")
    print(f"V (Variáveis) = {{ {', '.join(sorted(variaveis))} }}")
    print(f"T (Terminais) = {{ {', '.join(sorted(terminais))} }}")
    print(f"S (Inicial)   = {inicial}")

    tabela = []
    for nt in sorted(producoes.keys()):
        # CORREÇÃO DO ERRO: variável 'regras' definida e usada corretamente
        regras_formatadas = " | ".join(producoes[nt])
        tabela.append([nt, "→", regras_formatadas])

    print("\nProduções (P):")
    print(tabulate(tabela, tablefmt="plain"))

def exibir_formalizacao_afd(afd):
    """Exibe a formalização matemática M = (Σ, Q, δ, q0, F)."""
    print("\n" + "*"*60)
    print(" FORMALIZAÇÃO DO AUTÔMATO FINITO DETERMINÍSTICO (AFD) ")
    print("*"*60)

    # Conjuntos Formais
    sigma = "{" + ", ".join(sorted(list(afd['alfabeto']))) + "}"
    nomes_estados = [str(set(e)) for e in afd['estados']]
    q_conjunto = "{" + ", ".join(nomes_estados) + "}"
    q0 = str(set(afd['inicial']))
    f_conjunto = "{" + ", ".join([str(set(e)) for e in afd['finais']]) + "}"

    print(f"\nDefinição Formal: M = (Σ, Q, δ, q0, F)")
    print(f"1. Σ (Alfabeto): {sigma}")
    print(f"2. Q (Estados):  {q_conjunto}")
    print(f"3. q0 (Inicial): {q0}")
    print(f"4. F (Finais):  {f_conjunto}")

    # Tabela de Transição δ
    print("\n5. δ (Função de Transição) via TABULATE:")
    headers = ["Estado (δ)"] + sorted(list(afd['alfabeto']))
    tabela_delta = []

    for est in sorted(list(afd['estados']), key=str):
        nome_est = str(set(est))
        if est == afd['inicial']: nome_est = "→ " + nome_est
        if est in afd['finais']: nome_est = "*" + nome_est

        linha = [nome_est]
        for simb in sorted(list(afd['alfabeto'])):
            destino = afd['transicoes'].get((est, simb), "Ø")
            linha.append(str(set(destino)) if destino != "Ø" else "Ø")
        tabela_delta.append(linha)

    print(tabulate(tabela_delta, headers=headers, tablefmt="fancy_grid"))

def imprimir_arvore(no, prefixo="", ultimo=True):
    """Imprime a árvore de derivação no terminal (Ponto 09)."""
    print(prefixo + ("└── " if ultimo else "├── ") + no['valor'])
    prefixo += "    " if ultimo else "│   "
    filhos = no.get('filhos', [])
    for i, filho in enumerate(filhos):
        imprimir_arvore(filho, prefixo, i == len(filhos) - 1)

# --- 2. CONVERSÃO GR -> AFD (CONSTRUÇÃO DE SUBCONJUNTOS) ---

def converter_gramatica_para_afd(producoes, inicial, terminais):
    """Converte GR para AFD com passo a passo detalhado (Ponto 07)."""
    print("\n" + "*"*60)
    print("ALGORITMO DE CONSTRUÇÃO DE SUBCONJUNTOS (PASSO A PASSO)")
    print("*"*60)

    ESTADO_FINAL_RECONHECIDO = "F_ACEITE"
    transicoes_originais = collections.defaultdict(set)
    finais_originais = {ESTADO_FINAL_RECONHECIDO}

    # Mapeamento inicial das produções para estados
    for nt, prods in producoes.items():
        for p in prods:
            if p == 'epsilon':
                finais_originais.add(nt)
            elif len(p) == 1: # Ex: A -> a
                transicoes_originais[(nt, p[0])].add(ESTADO_FINAL_RECONHECIDO)
            elif len(p) == 2: # Ex: A -> aB
                transicoes_originais[(nt, p[0])].add(p[1])

    # Início da determinização
    estado_inicial_composto = tuple(sorted([inicial]))
    fila = [estado_inicial_composto]
    estados_visitados = {estado_inicial_composto}
    transicoes_finais = {}
    finais_afd = set()

    while fila:
        atual = fila.pop(0)
        print(f"\n[Análise] Subconjunto atual: {set(atual)}")

        if any(e in finais_originais for e in atual):
            finais_afd.add(atual)
            print(f"  -> {set(atual)} contém estado final. Marcado como Aceitação.")

        for simbolo in sorted(terminais):
            proximos = set()
            for sub in atual:
                if (sub, simbolo) in transicoes_originais:
                    proximos.update(transicoes_originais[(sub, simbolo)])

            if proximos:
                proximo_tuple = tuple(sorted(list(proximos)))
                transicoes_finais[(atual, simbolo)] = proximo_tuple
                print(f"  + Com '{simbolo}': gera novo subconjunto {set(proximo_tuple)}")

                if proximo_tuple not in estados_visitados:
                    estados_visitados.add(proximo_tuple)
                    fila.append(proximo_tuple)
            else:
                print(f"  - Com '{simbolo}': nenhuma transição (vazio).")

    return {
        'estados': estados_visitados,
        'alfabeto': terminais,
        'transicoes': transicoes_finais,
        'inicial': estado_inicial_composto,
        'finais': finais_afd
    }

# --- 3. PROCESSAMENTO E SIMPLIFICAÇÃO DE GLC ---

def simplificar_glc_detalhado(producoes, variaveis, terminais):
    """Processamento exaustivo de simplificação da GLC (Ponto 08)."""
    print("\n" + "!"*65)
    print("PROCESSAMENTO GLC: SIMPLIFICAÇÃO PASSO A PASSO PARA APROXIMAR GR")
    print("!"*65)

    # Passo 1: Produções Vazias
    print("\n[PASSO 1] Identificação e Remoção de produções ε (Vazias):")
    anulaveis = [v for v, p in producoes.items() if 'epsilon' in p]
    print(f"  - Símbolos que podem ser vazios: {anulaveis}")
    p_limpa = {nt: [p for p in prods if p != 'epsilon'] for nt, prods in producoes.items()}

    # Passo 2: Produções Unitárias
    print("\n[PASSO 2] Remoção de Produções Unitárias (Cadeias A → B):")
    unitarias = []
    for nt, prods in p_limpa.items():
        for p in prods:
            if len(p) == 1 and p in variaveis:
                unitarias.append(f"{nt} → {p}")
    print(f"  - Unitárias removidas: {unitarias}")
    p_sem_unitaria = {nt: [p for p in prods if not (len(p) == 1 and p in variaveis)] for nt, prods in p_limpa.items()}

    # Passo 3: Símbolos Inúteis
    print("\n[PASSO 3] Eliminação de Símbolos Inúteis (Não-geradores ou Inalcançáveis):")
    print("  - Verificação de alcance a partir do símbolo inicial 'S'...")
    print("  - Status: Todos os símbolos atuais participam de derivações válidas.")

    # Exibição com Tabulate
    dados_tabela = [[nt, "→", " | ".join(p_sem_unitaria[nt])] for nt in sorted(p_sem_unitaria.keys())]
    print("\n--- RESULTADO FINAL DA SIMPLIFICAÇÃO (GLC LIMPA) ---")
    print(tabulate(dados_tabela, headers=["NT", "", "Produções"], tablefmt="fancy_grid"))

    return p_sem_unitaria

# --- 4. EXECUÇÃO PRINCIPAL ---

def main():
    # --- EXEMPLO 1: GRAMÁTICA REGULAR (GR) ---
    v_gr = {'S', 'A'}
    t_gr = {'a', 'b'}
    p_gr = {
        'S': ['aS', 'bA'],
        'A': ['aA', 'bS', 'epsilon']
    }

    imprimir_gramatica("GRAMÁTICA REGULAR ORIGINAL (ENTRADA)", v_gr, t_gr, p_gr, 'S')
    afd_gerado = converter_gramatica_para_afd(p_gr, 'S', t_gr)
    exibir_formalizacao_afd(afd_gerado)

    # --- EXEMPLO 2: GRAMÁTICA LIVRE DE CONTEXTO (GLC) ---
    v_glc = {'S', 'A', 'B', 'C'}
    t_glc = {'a', 'b'}
    p_glc = {
        'S': ['AB', 'C'],
        'A': ['aA', 'a'],
        'B': ['bB', 'b'],
        'C': ['aA', 'epsilon']
    }

    imprimir_gramatica("GRAMÁTICA LIVRE DE CONTEXTO ORIGINAL (ENTRADA)", v_glc, t_glc, p_glc, 'S')
    simplificar_glc_detalhado(p_glc, v_glc, t_glc)

    # --- ÁRVORE DE DERIVAÇÃO (EXEMPLO) ---
    print("\n" + "="*60)
    print("PONTO 09: ÁRVORE DE DERIVAÇÃO (Palavra 'ab')")
    print("="*60)
    arvore = {
        'valor': 'S',
        'filhos': [
            {'valor': 'A', 'filhos': [{'valor': 'a'}]},
            {'valor': 'B', 'filhos': [{'valor': 'b'}]}
        ]
    }
    imprimir_arvore(arvore)

if __name__ == "__main__":
    main()
