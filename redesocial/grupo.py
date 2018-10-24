from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes

class Grupo:

    @classmethod
    def interagir_com_grupo(cls, id_interagido):
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
            ['Visitar Grupo']
            ]

        if not status:
            opcoes_grupo.append(['Solicitar Entrada'])
        elif status['status'] == 0:
            opcoes_grupo.append(['Cancelar Solicitação'])
        elif status['status'] == 1:
            opcoes_grupo.append(['Sair do Grupo'])

        opcao_grupo = menu_opcoes('INTERAGIR COM GRUPO', opcoes_grupo)

        if opcao_grupo == 1:
            pass # TODO: Visitar grupo
        elif opcao_grupo == 2:
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
