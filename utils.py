prefixo_menu = '\n>>> '
prefixo_opcao = '\t'


def menu_opcoes(titulo, opcoes):
    print(prefixo_menu, titulo)

    for i, opcao in enumerate(opcoes):
        print(prefixo_opcao, i, opcao[0])

    opcao = None
    while True:
        try:
            opcao = int(input('Escolha uma opção: '))
            if opcao < 0 or opcao >= len(opcoes):
                print('Opção inválida!')
                raise Exception()
        except:
            pass
        else:
            break

    return opcao
