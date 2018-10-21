from redesocial.registro import Credenciamento
from redesocial.login import LoginManager
from redesocial.utils import menu_opcoes
from redesocial.principal import MenuPrincipal
from redesocial import State


class MenuInicial():

    @classmethod
    def executar(cls):
        login_manager = LoginManager()
        credenciamento = Credenciamento()
        menu_principal = MenuPrincipal()

        while True:
            opcoes = [['Sair', None],
                      ['Registrar', credenciamento.registrar],
                      ['Login', login_manager.login]]

            opcao = menu_opcoes('MENU INICIAL', opcoes)

            if opcoes[opcao][1] is None:
                return

            opcoes[opcao][1]()

            if State.usuario_atual:
                menu_principal.executar()
