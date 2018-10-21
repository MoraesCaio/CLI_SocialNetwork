from redesocial import State
from redesocial.login import LoginManager
from redesocial.utils import menu_opcoes


class MenuPrincipal():

    @classmethod
    def executar(cls):
        login_manager = LoginManager()

        while True:
            opcoes = [['Logout', login_manager.logout],
                      ['Ver Perfil', None],
                      ['Ver Lista de Usuários', None],
                      ['Ver Lista de Grupos', None],]

            opcao = menu_opcoes('MENU INICIAL', opcoes)

            if opcoes[opcao][1] is None:
                return

            opcoes[opcao][1]()
