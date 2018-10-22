from redesocial import State
from redesocial.login import LoginManager
from redesocial.utils import menu_opcoes
from redesocial.database import DB
from redesocial.perfil import Perfil


class MenuPrincipal():

    @classmethod
    def executar(cls):
        login_manager = LoginManager()

        while True:
            opcoes = [['Logout', login_manager.logout],
                      ['Ver Perfil', cls.ver_perfil],
                      ['Ver Lista de Usuários', cls.ver_lista_usuarios],
                      ['Ver Lista de Grupos', None], ]

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
        db = DB()
        db.cursor.execute(f'SELECT name, city FROM tUser WHERE id_user != {State.usuario_atual["id_user"]}')
        users = db.cursor.fetchall()

        opcoes_usuarios = [['Cancelar']] + [[f'{user["name"]}, {user["city"]}'] for user in users]

        while True:
            opcao = menu_opcoes('USUÁRIOS DISPONÍVEIS PARA INTERAGIR', opcoes_usuarios)

            if not opcao:
                return
            else:
                # TODO
                return

    @classmethod
    def ver_lista_grupos(cls):
        pass