from redesocial.utils import menu_opcoes, imagem_blob
from redesocial import State
from redesocial.database import DB
from PIL import Image


class Credenciamento:

    msg_cancelamento = '(Para cancelar aperte Enter):\n'

    novo_usuario = {'nome': '', 'cidade': '', 'imagem': ''}

    @classmethod
    def registrar(cls):

        cls.novo_usuario['nome'] = ''
        cls.novo_usuario['cidade'] = ''
        cls.novo_usuario['imagem'] = ''

        opcoes = [['Cancelar', None],
                  ['Escolher nome', cls.definir_nome],
                  ['Escolher cidade', cls.definir_cidade],
                  ['Escolher imagem', cls.definir_imagem]]

        while not cls.novo_usuario['nome'] or \
                not cls.novo_usuario['cidade'] or \
                not cls.novo_usuario['imagem']:

            print('\nNome atual:', cls.novo_usuario['nome'])
            print('Cidade atual:', cls.novo_usuario['cidade'])
            print('Imagem atual:', cls.novo_usuario['imagem'])

            opcao = menu_opcoes('CADASTRO - Etapas', opcoes)

            if opcoes[opcao][1] is None:
                return

            opcoes[opcao][1]()

        DB.new_user(cls.novo_usuario['nome'], cls.novo_usuario['cidade'], cls.novo_usuario['imagem'])

        print('Usuário cadastrado!')

    @classmethod
    def definir_nome(cls):

        nome = input(f'Insira seu NOME com mais de 4 caracteres e menos de 255 caracteres. {cls.msg_cancelamento}')

        while True:
            if not len(nome):
                return
            elif len(nome) >= 255 or len(nome) < 4:
                nome = input(f'NOME inválido. Tente novamente {cls.msg_cancelamento}')
            else:
                cls.novo_usuario['nome'] = nome
                return

    @classmethod
    def definir_cidade(cls):
        cidade = input(f'Insira sua CIDADE com mais de 4 caracteres e menos de 255 caracteres. {cls.msg_cancelamento}')

        while True:
            if not len(cidade):
                return
            elif len(cidade) >= 255 or len(cidade) < 4:
                cidade = input(f'CIDADE inválida. Tente novamente. {cls.msg_cancelamento}')
            else:
                cls.novo_usuario['cidade'] = cidade
                return

    @classmethod
    def definir_imagem(cls):
        while True:
            path = input(f'Insira o caminho da sua IMAGEM de perfil. {cls.msg_cancelamento}')
            if not len(path):
                return
            else:
                try:
                    Image.open(path)
                except:
                    option = input('Não foi possível carregar a IMAGEM. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        cls.novo_usuario['imagem'] = State.imagem_usuario_padrao
                        return
                else:
                    cls.novo_usuario['imagem'] = path
                    return
