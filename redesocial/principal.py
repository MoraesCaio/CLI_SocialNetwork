from redesocial import State
from redesocial.login import LoginManager
from redesocial.utils import menu_opcoes
from redesocial.database import DB
from redesocial.perfil import Perfil
from redesocial.grupo import Grupo
from PIL import Image


class MenuPrincipal():

    novo_grupo = {'nome': '', 'descricao': '', 'imagem': '', 'visibilidade': 1}

    @classmethod
    def executar(cls):
        login_manager = LoginManager()

        while True:
            opcoes = [
                ['Logout', login_manager.logout],
                ['Ver Perfil', cls.ver_perfil],
                ['Ver Lista de Usuários', cls.ver_lista_usuarios],
                ['Ver Lista de Grupos', cls.ver_lista_grupos],
                ['Criar Grupo', cls.criar_grupo],
            ]

            opcao = menu_opcoes('MENU INICIAL', opcoes)

            opcoes[opcao][1]()

            if opcoes[opcao][1] == login_manager.logout:
                if State.usuario_atual is None:
                    return

    @classmethod
    def ver_perfil(cls):
        Perfil(State.usuario_atual).ver_menu()
        return

    @classmethod
    def ver_lista_usuarios(cls):
        DB.cursor.execute(f'''
            SELECT
                id_user, name, city
            FROM
                tUser
            WHERE
                id_user != {State.usuario_atual["id_user"]}
            ''')
        users = DB.cursor.fetchall()

        opcoes_usuarios = [['Cancelar']] + [[f'{user["name"]}, {user["city"]}'] for user in users]

        while True:
            opcao = menu_opcoes('USUÁRIOS DISPONÍVEIS PARA INTERAGIR', opcoes_usuarios)

            if not opcao:
                return
            else:
                Perfil.interagir_com_usuario(users[opcao - 1]['id_user'])
                return

    @classmethod
    def ver_lista_grupos(cls):
        DB.cursor.execute(f'SELECT * FROM tGroup')
        grupos = DB.cursor.fetchall()

        opcoes = [['Cancelar']] + [[f'{grupo["name"]}'] for grupo in grupos]
        opcao = menu_opcoes('INTERAGIR COM GRUPO', opcoes)

        if opcao != 0:
            Grupo(grupos[opcao - 1]['id_group']).ver_menu()

    @classmethod
    def criar_grupo(cls):
        opcoes = [
            ['Voltar', None],
            ['Definir Visibilidade do Grupo', cls.definir_visibilidade_grupo],
            ['Definir Nome do Grupo', cls.definir_nome_grupo],
            ['Definir Descrição do Grupo', cls.definir_descricao_grupo],
            ['Definir Imagem do Grupo', cls.definir_imagem_grupo]
        ]

        while not cls.novo_grupo['nome'] or \
                not cls.novo_grupo['descricao'] or \
                not cls.novo_grupo['imagem']:

            print('\nNome atual:', cls.novo_grupo['nome'])
            print('Descrição atual:', cls.novo_grupo['descricao'])
            print('Imagem atual:', cls.novo_grupo['imagem'])
            visi = cls.novo_grupo['visibilidade']
            print('Visibilidade atual:', ('Pública' if visi else 'Privada'))

            opcao = menu_opcoes('CRIAÇÃO DE GRUPO - Etapas', opcoes)

            if opcoes[opcao][1] is None:
                cls.novo_grupo['nome'] = ''
                cls.novo_grupo['descricao'] = ''
                cls.novo_grupo['imagem'] = ''
                cls.novo_grupo['visibilidade'] = 1
                return

            opcoes[opcao][1]()

        DB.new_group(cls.novo_grupo['nome'], cls.novo_grupo['descricao'], cls.novo_grupo['imagem'])

        print('Grupo cadastrado!')

    @classmethod
    def definir_visibilidade_grupo(cls):
        opcoes = [
            ['Cancelar'],
            ['Grupo Privado'],
            ['Grupo Público']
        ]

        while True:
            opcao = menu_opcoes('VISIBILIDADE DO GRUPO', opcoes)

            if not opcao:
                return
            elif type(opcao) == int:
                cls.novo_grupo['visibility'] = opcao - 1
                return

    @classmethod
    def definir_nome_grupo(cls):

        nome = input(f'Insira o NOME DO GRUPO com mais de 4 caracteres e menos de 255 caracteres. (ou Aperte ENTER para cancelar).')

        while True:
            if not len(nome):
                return
            elif len(nome) >= 255 or len(nome) < 4:
                nome = input(f'NOME DO GRUPO inválido. Tente novamente (ou Aperte ENTER para cancelar).')
            else:
                cls.novo_grupo['nome'] = nome
                return

    @classmethod
    def definir_descricao_grupo(cls):
        descricao = input(f'Insira a DESCRIÇÃO DO GRUPO com mais de 4 caracteres e menos de 255 caracteres. (ou Aperte ENTER para cancelar)')

        while True:
            if not len(descricao):
                return
            elif len(descricao) >= 255 or len(descricao) < 4:
                descricao = input(f'DESCRIÇÃO DO GRUPO inválida. Tente novamente. (ou Aperte ENTER para cancelar)')
            else:
                cls.novo_grupo['descricao'] = descricao
                return

    @classmethod
    def definir_imagem_grupo(cls):
        while True:
            path = input(f'Insira o caminho da IMAGEM DO GRUPO. (ou Aperte ENTER para cancelar)')
            if not len(path):
                return
            else:
                try:
                    Image.open(path)
                except:
                    option = input('Não foi possível carregar a IMAGEM DO GRUPO. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        cls.novo_grupo['imagem'] = State.imagem_grupo_padrao
                        return
                else:
                    cls.novo_grupo['imagem'] = path
                    return
