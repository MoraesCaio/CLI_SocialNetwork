from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem


class Grupo():

    db = DB()
    grupo = None

    @classmethod
    def __init__(cls, grupo):
        if type(grupo) == int:
            id_group = grupo
            cls.db.cursor.execute(f'SELECT * FROM tUser WHERE id_group = {id_group}')
            cls.grupo = cls.db.fetchone()
        elif type(grupo) == dict:
            cls.grupo = grupo

    @classmethod
    def ver_menu(cls):
        print(f"Nome: {cls.grupo['name']}")
        print(f"Descrição: {cls.grupo['description']}")

    @classmethod
    def configuracoes_grupo(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.grupo)

    @classmethod
    def ver_membros(cls):
        pass

    @classmethod
    def ver_solicitacoes(cls):
        pass

    @classmethod
    def ver_mural(cls):
        pass
