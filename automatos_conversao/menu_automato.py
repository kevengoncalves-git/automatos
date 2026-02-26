print("-"*50)
print("Bem vindo ao conversor e validador de autômatos")
print("-"*50)

def menu():
    while True:
        print("\nEscolha uma opção:")
        print("1 - Definir um AFD")
        print("2 - Definir um AFND")
        print("3 - Converter AFND para AFD")
        print("4 - Minimizar um AFD")
        print("5 - Usar AFND pré-definido para teste")
        print("6 - Sair")

        try:
            opcao = int(input("Opção: "))
            if opcao in [1, 2, 3, 4, 5, 6]:
                return opcao
            else:
                print("Opção inválida.")
        except ValueError:
            print("Digite um número válido.")
            
def menu_secundario():
    while True:
        print("1 - Validar palavra")
        print("2 - Voltar pro Menu Principal")
        print("3 - Sair")

        try:
            opcao = int(input("Opção: "))
            if opcao in [1, 2, 3]:
                return opcao
            else:
                print("Opção inválida.")
        except ValueError:
            print("Digite um número válido.")