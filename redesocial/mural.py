import os
from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem, imagem_blob


class Mural():

    id_mural = None

    @classmethod
    def __init__(cls, id_mural):
        cls.id_mural = id_mural

    @classmethod
    def fazer_postagem(cls):
        print('NOVA POSTAGEM')
        text = input('Texto: ')
        img_path = input('Path para imagem: ')

        if not os.path.isfile(img_path):
            img_blob = None
        else:
            img_blob = imagem_blob(img_path)

        if text or img_blob:
            DB.cursor.execute('''
                INSERT INTO
                    tPost(id_wall, id_user, text, image)
                VALUES
                    (%s, %s, %s, %s)
                ''', (cls.id_mural, State.usuario_atual['id_user'], text, img_blob)
                )
            print('Postagem feita.')
            DB.connection.commit()

    @classmethod
    def fazer_comentario(cls, id_post):
        print('NOVO COMENTÁRIO')
        text = str(input('Texto: '))

        if text:
            DB.cursor.execute('''
                INSERT INTO
                    tComment(id_post, id_user, text)
                VALUES
                    (%s, %s, %s)
                ''', (id_post, State.usuario_atual['id_user'], text)
                )
            print('Comentário feito.')
            DB.connection.commit()
        else:
            print('O campo de texto não pode ser vazio.')

    @classmethod
    def fazer_resposta(cls, id_comment):
        print('NOVA RESPOSTA')
        text = str(input('Texto: '))

        if text:
            DB.cursor.execute('''
                INSERT INTO
                    tReply(id_comment, id_user, text)
                VALUES
                    (%s, %s, %s)
                ''', (id_comment, State.usuario_atual['id_user'], text)
                )
            print('Resposta feita.')
            DB.connection.commit()
        else:
            print('O campo de texto não pode ser vazio.')
