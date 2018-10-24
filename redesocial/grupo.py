from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem


class Grupo():

    grupo = None

    @classmethod
    def __init__(cls, grupo):
        if type(grupo) == int:
            id_group = grupo
            DB.cursor.execute(f'SELECT * FROM tGroup WHERE id_group = {id_group}')
            cls.grupo = DB.cursor.fetchone()
        elif type(grupo) == dict:
            cls.grupo = grupo

    @classmethod
    def ver_menu(cls):
        print(f"Nome: {cls.grupo['name']}")
        print(f"Descrição: {cls.grupo['description']}")

        cls.interagir_com_grupo(cls.grupo['id_group'])

    @classmethod
    def interagir_com_grupo(cls, id_interagido):
        # TODO: Integrar à função ver_menu e excluir essa.
        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {id_interagido}
            ''')
        status = DB.cursor.fetchone()

        opcoes_grupo = [
            ['Cancelar'],
            ['Visitar Grupo'],
            ['Ver Membros']
            ]

        if not status:
            opcoes_grupo.append(['Solicitar Entrada'])
        elif status['status'] == 0:
            opcoes_grupo.append(['Cancelar Solicitação'])
        elif (status['status'] == 1 or status['status'] == 2):
            opcoes_grupo.append(['Sair do Grupo'])

        DB.cursor.execute(f'''
            SELECT
                status
            FROM
                rUser_Group
            WHERE
                id_user = {State.usuario_atual['id_user']}
            AND
                id_group = {id_interagido}
            AND
                status = 2
            ''')

        is_admin = True if DB.cursor.fetchone() else None

        if is_admin:
            opcoes_grupo.append(['Ver Solicitações'])

        opcao_grupo = menu_opcoes('INTERAGIR COM GRUPO', opcoes_grupo)

        if opcao_grupo == 1:
            pass # TODO: Visitar grupo
        elif opcao_grupo == 2:
            cls.ver_membros()
        elif opcao_grupo == 3:
            if not status:
                # Solicitar entrada
                DB.cursor.execute(f'''
                    INSERT INTO
                        rUser_Group(id_user, id_group, status)
                    VALUES
                        ({State.usuario_atual['id_user']}, {id_interagido}, 0)
                    ''')
                print('Solicitação enviada.')
                DB.connection.commit()
            elif status['status'] == 0:
                # Cancelar solicitação
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {State.usuario_atual['id_user']}
                    AND
                        id_group = {id_interagido}
                    ''')
                print('Solicitação cancelada.')
                DB.connection.commit()
            elif status['status'] == 1:
                # Sair do grupo
                DB.cursor.execute(f'''
                    DELETE FROM
                        rUser_Group
                    WHERE
                        id_user = {State.usuario_atual['id_user']}
                    AND
                        id_group = {id_interagido}
                    ''')
                print('Você saiu desse grupo.')
                DB.connection.commit()
        elif opcao_grupo == 4:
            cls.ver_solicitacoes()

    @classmethod
    def configuracoes_grupo(cls):
        pass

    @classmethod
    def ver_foto(cls):
        ver_imagem(cls.grupo)

    @classmethod
    def ver_membros(cls):
        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                rUser_Group
            INNER JOIN
                tUser
            ON
                rUser_Group.id_user = tUser.id_user
            WHERE
                id_group = {cls.grupo['id_group']}
            AND
                (status = 1 OR status = 2)
            ''')

        membros = DB.cursor.fetchall()
        opcoes = [['Cancelar']] + [[f'{membro["name"]}'] for membro in membros]
        opcao = menu_opcoes('INTERAGIR COM MEMBRO', opcoes)
        # TODO: tratar opção


    @classmethod
    def ver_solicitacoes(cls):
        DB.cursor.execute(f'''
            SELECT
                *
            FROM
                rUser_Group
            INNER JOIN
                tUser
            ON
                rUser_Group.id_user = tUser.id_user
            WHERE
                id_group = {cls.grupo['id_group']}
            AND
                status = 0
            ''')

        solicitacoes = DB.cursor.fetchall()
        opcoes = [['Cancelar']] + [[f'{solicitacao["name"]}'] for solicitacao in solicitacoes]
        opcao = menu_opcoes('INTERAGIR COM SOLICITAÇÃO', opcoes)
        # TODO: tratar opção


    @classmethod
    def ver_mural(cls):
        pass
