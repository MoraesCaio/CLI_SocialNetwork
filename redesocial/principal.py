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
                      ['Ver Lista de Grupos', cls.ver_lista_grupos], ]

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
        DB.cursor.execute(f'''
            SELECT
                id_user, name, city
            FROM
                tUser
            WHERE
                id_user != {State.usuario_atual["id_user"]}
            ''')
        users = DB.cursor.fetchall()

        opcoes_usuarios = [['Cancelar']] + [[f'{user["name"]}, {user["city"]}'] for user in users]

        while True:
            opcao = menu_opcoes('USUÁRIOS DISPONÍVEIS PARA INTERAGIR', opcoes_usuarios)

            if not opcao:
                return
            else:
                # TODO
                Perfil.interagir_com_usuario(users[opcao - 1]['id_user'])
                return

    @classmethod
    def ver_lista_grupos(cls):
        DB.cursor.execute(f'SELECT * FROM tGroup')
        grupos = DB.cursor.fetchall()

        opcoes = [['Cancelar']] + [[f'{grupo["name"]}'] for grupo in grupos]
        opcao = menu_opcoes('INTERAGIR COM GRUPO', opcoes)

        if opcao != 0:
            DB.cursor.execute(f'''
                SELECT
                    status
                FROM
                    rUser_Group
                WHERE
                    id_user = {State.usuario_atual['id_user']}
                AND
                    id_group = {grupos[opcao - 1]['id_group']}
                ''')
            status = DB.cursor.fetchone()

            opcoes_grupo = [
                ['Cancelar'],
                ['Visitar Grupo']
                ]

            if status:
                if status == 0:
                    opcoes_grupo.append(['Cancelar Solicitação'])
                elif status == 1:
                    opcoes_grupo.append(['Sair do Grupo'])
            else:
                opcoes_grupo.append(['Solicitar Entrada'])

            opcao_grupo = menu_opcoes('INTERAGIR COM GRUPO', opcoes_grupo)
            # TODO: tratar seleção
