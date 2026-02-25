# imprimir a arvore bonitinha
def imprimir_arvore_visual(simbolo, lista_regras, prefixo="", ultimo=True, raiz=True):
    #funcao recursiva que desenha a arvore no terminal
    # condicao 1 -> imprime o no atual com os galhos corretos
    if raiz:
        print(simbolo)
    else:
        marcador = "└── " if ultimo else "├── "
        print(prefixo + marcador + simbolo)

    # condicao 2 -> se for uma letra maiusucla (variavel) e tivermos regras na memoria
    if simbolo.isupper() and len(lista_regras) > 0:
        # puxa a proxima regra que a varredura descobriu para usar
        # pop(0) por conta da derivacao a esquerda
        variavel, producao = lista_regras.pop(0)

        #condicao 3 -> calcula o espaco para os filhos do no
        if raiz:
            novo_prefixo = ""
        else:
            # se esse no for o ultimo filho o espaco dele é vazio
            #se ele ter irmao abaixo, desce uma linha reta
            novo_prefixo = prefixo + ("  " if ultimo else "│" )

        # condicao 4 -> recursao para desenhar os fihos
        for i, char in enumerate(producao):
            filho_ultimo = (i ==len(producao) -1)
            imprimir_arvore_visual(char, lista_regras, novo_prefixo, filho_ultimo, False)

# gerar arvore derivacao (alteracoes feitas para imprimir a arvore e correcao de ortografia)
def gerar_arvore_derivacao(gramatica, palavra_alvo):
    print("="*40)
    print(f"Arvore de derivacao para: '{palavra_alvo}'")
    print("="*40)

    inicial = gramatica["inicial"]
    regras = gramatica["regras"]

    # funcao recursiva que faz o backtracking 
    def derivar(forma_atual, passos_str, regras_usadas):
        # condicao 1 -> sucesso na palavra alvo, agora varredura
        if forma_atual == palavra_alvo:
            # agora retorna a lista de regras usadas
            return passos_str, regras_usadas
        
        # condicao 2 -> parada p evitar o loop infinito
        if len(forma_atual) > len(palavra_alvo):
            return None, None
        
        # condicao 3 -> encontrar o primeiro nao-terminal p/ substituir
        nao_terminal_alvo = None
        indice_substituicao = -1

        for i, char in enumerate(forma_atual):
            if char.isupper():
                nao_terminal_alvo = char
                indice_substituicao =i
                break
        # tem minuscula, mas nao é a palavra alvo
        if nao_terminal_alvo is None:
            return None, None
        
        #condicao 4 -> tentar aplicar as regras para o nao-terminal *
        if nao_terminal_alvo in regras:
            for nome_regra, producao in regras[nao_terminal_alvo].items():
                # cria a nova string p substituir a letra maiuscula pela producao
                nova_forma = forma_atual[:indice_substituicao] + producao + forma_atual[indice_substituicao + 1:]
                
                # novo passo a passo com a flechinha =>
                novo_passos_str = regras_usadas + [f" => {nova_forma} (usando {nao_terminal_alvo} -> {producao})"]

                # guarda a regra que esta tentando usar ('S', 'aA')
                nova_regras_usadas = regras_usadas + [(nao_terminal_alvo, producao)]

                # entraando na recursao
                res_passos, res_regras = derivar(nova_forma, novo_passos_str, nova_regras_usadas)

                #se retornar caminho valido o sucesso vai pra cima
                if res_passos is not None:
                    return res_passos, res_regras
        # se deu ruim em todas as regras
        return None, None
    
    # recursao comecando pelo simbolo incial S
    caminho_sucesso, regras_sucesso = derivar(inicial, [f" {inicial} (Simbolo Inicial)"], [])
    
    # exibir o resultado final
    if caminho_sucesso is not None:
        print("1. Palavra gerado com sucesso. Gerando passo a passo: \n")
        for passo in caminho_sucesso:
            print(passo)
        
        print("2. Arvore Visual Gerada")
        # chama o a def de imprimir a arvore visual passando o simbolo inicial e copia das regras encontradas
        imprimir_arvore_visual(inicial, list(regras_sucesso))
    else:
        print(f"A palavra '{palavra_alvo}' Nao pode ser gerada por esta gramatica")
    print("-"*40)

# teste
gramatica_teste = {
    "inicial": "S",
    "regras": {
        "S": {"r1": "aA", "r2": "b"},
        "A": {"r1": "aS", "r2": "b"}
    }
}

#palabra que existe
gerar_arvore_derivacao(gramatica_teste, "aab")

#teste2 palabra que n existe
#gerar_arvore_derivacao(gramatica_teste, "aba")