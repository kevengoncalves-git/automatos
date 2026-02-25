# simular codigo keve
#gramatica_teste = {
 #   "inicial": "S",
  #  "regras": {
   #     # dicionario dentro dicionario
    #    "S": {"regra1": "aA", "regra2": "b"},
     #   "A": {"regra1": "aS", "regra2": "b"}
    #}
#}

def gerar_pseudocodigo_reconhecer(gramatica):
    print("="*40)
    print("pseudocodigo do reconhecedor gerado")
    print("="*40)

    regras = gramatica["regras"]

    #adicionando uma funcao principal para startar
    estado_inicial = gramatica["inicial"]
    print(f"funcao principal():")
    print(f"inicialzar_leitura_da_palavra()")
    print(f"chamar_{estado_inicial}()")
    print(f"se fim_da_palabra():")
    print(f" retornar SUCESSO()")
    print(f" senao:")
    print(f" retonar ERRO")
    print("-" * 40)

    # gerando funcoes para os nao terminais
    for nao_terminal, dict_producoes in regras.items():
        print(f"\nfuncao chamar_{nao_terminal}()")
        print("cabeca = ler_simbolo_atual()")
        print( "escolha (cabeca):")

        # dicionatio interno (regra1, aA)
        for nome_da_regra, producao in dict_producoes.items():
            primeiro_simbolo = producao[0]
            print(f"caso '{primeiro_simbolo}': //aplicando {nao_terminal} -> {producao} ")

            # analisa cada letra da producao
            for simbolo in producao:
                if simbolo.islower(): # e terminal: letra minuscula
                    print(f"casar('{simbolo}')")
                elif simbolo.isupper(): # e um nao-terminal: letra maiscula
                    print(f"chamar_{simbolo}()")
        #caso o simbolo n seja condiza com nenhuma regra
        print("padrao")
        print("retornar ERRO_DE_SINTAXE")

# simular codigo keve
gramatica_teste = {
    "inicial": "S",
    "regras": {
        "S": {"r1": "aA", "r2": "b"},
        "A": {"r1": "aS", "r2": "b"}
    }
}

gerar_pseudocodigo_reconhecer(gramatica_teste)