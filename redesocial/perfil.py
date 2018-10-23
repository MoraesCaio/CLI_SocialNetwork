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
            cls.owner_user = DB.cursor.fetchone()
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
                tUser.id_user, tUser.name, tUser.city
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
                tUser.id_user, tUser.name, tUser.city
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
            opcoes = [['Cancelar']] + [[f'''{amigo['name']}, de {amigo['city']}'''] for amigo in amigos]
            opcao = menu_opcoes('AMIGOS', opcoes)
            if opcao != 0:
                # Ver status do usuário selecionado com o usuário logado
                DB.cursor.execute(f'''
                    -- Lado esquerdo do relacionamento
                    SELECT
                        *
                    FROM
                        rUser_User
                    WHERE
                        id_user_from = {amigos[opcao - 1]['id_user']}
                    AND
                        id_user_to = {State.usuario_atual['id_user']}
                    UNION

                    -- Lado direito do relacionamento
                    SELECT
                        *
                    FROM
                        rUser_User
                    WHERE
                        id_user_to = {amigos[opcao - 1]['id_user']}
                    AND
                        id_user_from = {State.usuario_atual['id_user']}

                    ''')
                status_dos_usuarios = DB.cursor.fetchone()

                opcoes = [
                        ['CANCELAR'],
                        ['VISITAR PERFIL'],
                        ['SOLICITAR AMIZADE'] if not status_dos_usuarios else ['DESFAZER AMIZADE'],
                        ['BLOQUEAR']
                        ]
                opcao_usuario = menu_opcoes(f'''INTERAGIR COM {amigos[opcao - 1]['name']}''', opcoes)
                if opcao_usuario != 0:
                    if opcao_usuario == 1:
                        pass # TODO: visitar perfil
                    elif opcao_usuario == 2:
                        if not status_dos_usuarios:
                            # Solicitar amizade
                            DB.cursor.execute(f'''
                                INSERT INTO
                                    rUser_User(id_user_from, id_user_to, status)
                                VALUES
                                    ({State.usuario_atual['id_user']}, {amigos[opcao - 1]['id_user']}, 0)
                            ''')
                            print('Amizade solicitada!')
                        else:
                            # Desfazer amizade
                            DB.cursor.execute(f'''
                                DELETE FROM
                                    rUser_user
                                WHERE (
                                    id_user_from = {State.usuario_atual['id_user']}
                                AND
                                    id_user_to = {amigos[opcao - 1]['id_user']}
                                )
                                OR (
                                     id_user_to = {State.usuario_atual['id_user']}
                                AND
                                    id_user_from = {amigos[opcao - 1]['id_user']}
                                )
                            ''')
                            print('Amizade desfeita.')
                    elif opcao_usuario == 3:
                        if status_dos_usuarios:
                            # Bloqueio quando os usuários já são amigos
                            DB.cursor.execute(f'''
                                UPDATE
                                    rUser_User
                                SET
                                    status = 2
                                WHERE (
                                    id_user_from = {State.usuario_atual['id_user']}
                                AND
                                    id_user_to = {amigos[opcao - 1]['id_user']}
                                )
                                OR (
                                     id_user_to = {State.usuario_atual['id_user']}
                                AND
                                    id_user_from = {amigos[opcao - 1]['id_user']}
                                )
                                ''')
                        else:
                            # Bloqueio quando não sao amigos
                            DB.cursor.execute(f'''
                            INSERT INTO
                                rUser_User(id_user_from, id_user_to, status)
                            VALUES
                                ({State.usuario_atual['id_user']}, {amigos[opcao - 1]['id_user']}, 2)
                            ''')
        else:
            print('Esse usuário não tem amigos.')

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
