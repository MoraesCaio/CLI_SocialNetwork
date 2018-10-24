from redesocial import State
from redesocial.login import LoginManager
from redesocial.utils import menu_opcoes
from redesocial.database import DB
from redesocial.perfil import Perfil
from redesocial.grupo import Grupo


class MenuPrincipal():

    @classmethod
    def executar(cls):
        login_manager = LoginManager()

        while True:
            opcoes = [['Logout', login_manager.logout],
                      ['Ver Perfil', cls.ver_perfil],
                      ['Ver Lista de Usuários', cls.ver_lista_usuarios],
                      ['Ver Lista de Grupos', cls.ver_lista_grupos], ]

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
