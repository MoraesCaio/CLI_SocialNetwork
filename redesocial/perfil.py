from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem


class Perfil():

    db = DB()
    owner_user = None

    @classmethod
    def __init__(cls, user):
        if type(user) == int:
            id_user = user
            cls.db.cursor.execute(f'SELECT * FROM tUser WHERE id_user = {id_user}')
            cls.owner_user = cls.db.fetchone()
        elif type(user) == dict:
            cls.owner_user = user

    @classmethod
    def ver_menu(cls):
        print('\n---- PERFIL ----')
        print(f"Nome: {cls.owner_user['name']}")
        print(f"Cidade: {cls.owner_user['city']}")

    @classmethod
    def configuracoes_conta(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.owner_user)

    @classmethod
    def ver_amigos(cls):
        pass

    @classmethod
    def ver_grupos(cls):
        pass

    @classmethod
    def ver_solicitacoes(cls):
        pass

    @classmethod
    def ver_mural(cls):
        pass

    @classmethod
    def criar_grupo(cls):
        pass
