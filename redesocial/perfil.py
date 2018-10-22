from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem


class Perfil():

    owner_user = None

    @classmethod
    def __init__(cls, user):
        if type(user) == int:
            id_user = user
            DB.cursor.execute(f'SELECT * FROM tUser WHERE id_user = {id_user}')
            cls.owner_user = DB.fetchone()
        elif type(user) == dict:
            cls.owner_user = user

    @classmethod
    def ver_menu(cls):
        print('\n---- PERFIL ----')
        print(f"Nome: {cls.owner_user['name']}")
        print(f"Cidade: {cls.owner_user['city']}")

        cls.ver_amigos()
        cls.ver_grupos()

    @classmethod
    def configuracoes_conta(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.owner_user)

    @classmethod
    def ver_amigos(cls):
        DB.cursor.execute(f'''
            -- Os convites de amizade confirmados que essa pessoa fez
            SELECT
                tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_to = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_from = {cls.owner_user['id_user']}

            UNION

            -- Os convites de amizade que essa pessoa aceitou
            SELECT
                tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_User.id_user_from = tUser.id_user
            WHERE
                status = 1
            AND
                id_user_to = {cls.owner_user['id_user']}
            ''')
        amigos = DB.cursor.fetchall()

        if amigos:
            print('Amigos:')
            for amigo in amigos:
                print(f'''-> {amigo['name']}, de {amigo['city']}''')

    @classmethod
    def ver_grupos(cls):
        DB.cursor.execute(f'''
            SELECT
                tGroup.name, status
            FROM
                rUser_Group
            INNER JOIN
                tGroup
            ON
                rUser_Group.id_group = tGroup.id_group
            WHERE
                id_user = {cls.owner_user['id_user']}
            ''')
        grupos = DB.cursor.fetchall()

        if grupos:
            print('Grupos:')
            for grupo in grupos:
                print(f'''-> {grupo['name']}''')

    @classmethod
    def ver_solicitacoes(cls):
        DB.cursor.execute(f'''
            SELECT
                tUser.id_user, tUser.name, tUser.city
            FROM
                rUser_User
            INNER JOIN
                tUser
            ON
                rUser_user.id_user_from = tUser.id_user
            WHERE
                id_user_to = {cls.owner_user['id_user']}
            ''')
        solicitacoes = DB.cursor.fetchall()

        if solicitacoes:
            for solicitacao in solicitacoes:
                print(solicitacao)

    @classmethod
    def ver_mural(cls):
        pass

    @classmethod
    def criar_grupo(cls):
        pass
