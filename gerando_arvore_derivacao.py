# gerar arvore derivacao
def gerar_arvore_derivacao(gramatica, palavvra_alvo):
    print("="*40)
    print(f"Arvore de derivacao para: '{palavvra_alvo}'")
    print("="*40)

    inicial = gramatica["inicial"]
    regras = gramatica["regras"]

    # funcao recursiva que faz o backtracking 
    def derivar(forma_atual, historico):
        # condicao 1 -> sucesso na palabra alvo
        if forma_atual == palavvra_alvo:
            return historico
        
        # condicao 2 -> parada p evitar o loop infinito
        if len(forma_atual) > len(palavvra_alvo):
            return None
        
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
            return None
        
        #condicao 4 -> tentar aplicar as regras para o nao-terminal
        if nao_terminal_alvo in regras:
            for a_regra, producao in regras[nao_terminal_alvo].items():
                # cria a nova string p substituir a letra maiuscula pela producao
                nova_forma = forma_atual[:indice_substituicao] + producao + forma_atual[indice_substituicao + 1:]
                # passo a passo com a flechinha =>
                novo_historico = historico + [f" => {nova_forma} (usando {nao_terminal_alvo} -> {producao})"]
                #recursao da nova stringn
                resultado = derivar(nova_forma, novo_historico)

                #se retornar caminho valido o sucesso vai pra cima
                if resultado is not None:
                    return resultado
        # se deu ruim em todas as regras
        return None
    # recursao comecando pelo simbolo incial S
    caminho_sucesso = derivar(inicial, [f" {inicial} (simbolo inicial)"])
    
    # exibir o resultado final
    if caminho_sucesso:
        print("Palavra gerado com sucesso. gerando passo a passo: \n")
        for passo in caminho_sucesso:
            print(passo)
    else:
        print(f"A palavra '{palavvra_alvo}' nao pode ser gerada por esta gramatica")
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
gerar_arvore_derivacao(gramatica_teste, "aba")