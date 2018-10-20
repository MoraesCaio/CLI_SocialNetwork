from utils import menu_opcoes
from PIL import Image


class Credenciamento:

    imagem_padrao = 'default.jpg'
    msg_cancelamento = '(Para cancelar aperte Enter):\n'

    novo_usuario = {'nome': '', 'cidade': '', 'imagem': ''}

    def registrar(self):

        opcoes = [['Cancelar', None],
                  ['Escolher nome', self.definir_nome],
                  ['Escolher cidade', self.definir_cidade],
                  ['Escolher imagem', self.definir_imagem]]

        while not self.novo_usuario['nome'] or \
                not self.novo_usuario['cidade'] or \
                not self.novo_usuario['imagem']:

            print('\nNome atual:', self.novo_usuario['nome'])
            print('Cidade atual:', self.novo_usuario['cidade'])
            print('Imagem atual:', self.novo_usuario['imagem'])

            opcao = menu_opcoes('CADASTRO - Etapas', opcoes)

            if opcoes[opcao][1] is None:
                return

            opcoes[opcao][1]()

        # TODO add sql queries!
        print('Usuário cadastrado!')

    def definir_nome(self):

        nome = input(f'Insira seu NOME com mais de 4 caracteres e menos de 255 caracteres. {self.msg_cancelamento}')

        while True:
            if not len(nome):
                return
            elif len(nome) >= 255 or len(nome) < 4:
                nome = input(f'NOME inválido. Tente novamente {self.msg_cancelamento}')
            else:
                self.novo_usuario['nome'] = nome
                return

    def definir_cidade(self):
        cidade = input(f'Insira sua CIDADE com mais de 4 caracteres e menos de 255 caracteres. {self.msg_cancelamento}')

        while True:
            if not len(cidade):
                return
            elif len(cidade) >= 255 or len(cidade) < 4:
                cidade = input(f'CIDADE inválida. Tente novamente. {self.msg_cancelamento}')
            else:
                self.novo_usuario['cidade'] = cidade
                return

    def definir_imagem(self):
        while True:
            path = input(f'Insira o caminho da sua IMAGEM de perfil. {self.msg_cancelamento}')
            if not len(path):
                return
            else:
                try:
                    Image.open(path)
                except:
                    option = input('Não foi possível carregar a IMAGEM. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        self.novo_usuario['imagem'] = self.imagem_padrao
                        return
                else:
                    self.novo_usuario['imagem'] = path
                    return
