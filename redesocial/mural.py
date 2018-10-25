import os
from redesocial import State
from redesocial.database import DB
from redesocial.utils import menu_opcoes, ver_imagem, imagem_blob
from PIL import Image


class Mural():

    id_mural = None

    @classmethod
    def __init__(cls, id_mural):
        cls.id_mural = id_mural

    @classmethod
    def fazer_postagem(cls):
        print('NOVA POSTAGEM')
        while True:
            text = input('Texto: ')
            if len(text) > 0 or len(text) < 255:
                break

        while True:
            img_path = input('Path para IMAGEM DO POST: ')
            if not len(img_path):
                return
            else:
                try:
                    Image.open(img_path)
                except:
                    option = input('Não foi possível carregar a IMAGEM DO POST. Deseja utilizar a imagem padrão? [s/N]')
                    if option.lower() == 's':
                        img_path = State.imagem_post_padrao
                        break
                else:
                    break

        img_blob = imagem_blob(img_path)

        DB.cursor.execute('''
            INSERT INTO
                tPost(id_wall, id_user, text, image)
            VALUES
                (%s, %s, %s, %s)
            ''', (cls.id_mural, State.usuario_atual['id_user'], text, img_blob)
        )
        DB.connection.commit()
        print('Postagem feita.')

    @classmethod
    def fazer_comentario(cls, id_post):
        print('NOVO COMENTÁRIO')
        text = str(input('Texto: '))

        if text:
            DB.cursor.execute('''
                INSERT INTO
                    tComment(id_wall, id_post, id_user, text)
                VALUES
                    (%s, %s, %s, %s)
                ''', (cls.id_mural, id_post, State.usuario_atual['id_user'], text)
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
                    tReply(id_wall, id_comment, id_user, text)
                VALUES
                    (%s, %s, %s, %s)
                ''', (cls.id_mural, id_comment, State.usuario_atual['id_user'], text)
            )
            print('Resposta feita.')
            DB.connection.commit()
        else:
            print('O campo de texto não pode ser vazio.')
