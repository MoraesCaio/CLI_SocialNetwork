from database import DB
from registro import Credenciamento
from login import LoginManager
from utils import menu_opcoes


def inicial():
    login_manager = Login_Manager()
    credenciamento = Credenciamento()

    while True:
        opcoes = [['Sair', None],
                  ['Registrar', credenciamento.registrar],
                  ['Login', login_manager.login]]

        opcao = menu_opcoes('MENU INICIAL', opcoes)

        if opcoes[opcao][1] is None:
            return

        opcoes[opcao][1]()


if __name__ == '__main__':
    inicial()
