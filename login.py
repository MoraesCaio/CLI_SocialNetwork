from database import DB
from utils import menu_opcoes


class Login_Manager:

    usuario_atual = None

    def login(self):
        db = DB()
        db.cursor.execute('SELECT name, city FROM tUser')
        users = db.cursor.fetchall()

        opcoes = [['Cancelar']] + [[f'{user["name"]}, {user["city"]}'] for user in users]

        opcao = menu_opcoes('USUÁRIOS DISPONÍVEIS PARA LOGIN', opcoes)

        if not opcao:
            return
        else:
            db.cursor.execute(f'SELECT * FROM tUser WHERE id_user={opcao}')
            self.usuario_atual = db.cursor.fetchone()
            print(f'\nLOGADO COMO: {self.usuario_atual["name"]}')

    def logout(self):
        opcao = input('DESEJA REALIZAR LOGOUT? [s/N]')

        if opcao.lower() == 's':
            self.usuario_atual = None
            print('LOGOUT REALIZADO COM SUCESSO!')
