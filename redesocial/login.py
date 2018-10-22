from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes


class LoginManager:

    @classmethod
    def login(cls):
        DB.cursor.execute('SELECT name, city FROM tUser')
        users = DB.cursor.fetchall()

        opcoes = [['Cancelar']] + [[f'{user["name"]}, {user["city"]}'] for user in users]

        opcao = menu_opcoes('USUÁRIOS DISPONÍVEIS PARA LOGIN', opcoes)

        if not opcao:
            return
        else:

            DB.cursor.execute(f'SELECT * FROM tUser WHERE id_user={opcao}')

            if State.usuario_atual is None:
                State.usuario_atual = DB.cursor.fetchone()
            else:
                new_login = DB.cursor.fetchone()
                opcao = input(f'Você já está logado como {State.usuario_atual["name"]}. Deseja logar como {new_login["name"]}? [S/n]: ')

                if opcao.lower() != 'n':
                    State.usuario_atual = new_login

            print(f'\nVOCÊ ESTÁ LOGADO COMO: {State.usuario_atual["name"]}')

            return

    @classmethod
    def logout(cls):
        opcao = input('DESEJA REALIZAR LOGOUT? [s/N]')

        if opcao.lower() == 's':
            State.usuario_atual = None
            print('LOGOUT REALIZADO COM SUCESSO!')
