import base64
import os
from PIL import Image

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


def ver_imagem(entidade):
    tmp_file = 'tmp.jpg'
    with open(tmp_file, 'w+b') as f:
        f.write(base64.b64decode(entidade['img']))
    Image.open(tmp_file).show()
    os.remove(tmp_file)
