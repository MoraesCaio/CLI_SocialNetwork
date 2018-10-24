import pymysql
import os
from redesocial.utils import imagem_blob


class DB:
    connection = None
    cursor = None

    @classmethod
    def __init__(cls):
        if cls.connection is None or cls.cursor is None:
            cls.connection = pymysql.connect(
                host='127.0.0.1',
                db='myface_schema',
                user='myfaceAdm',
                password='myfaceAdm',
                cursorclass=pymysql.cursors.DictCursor
            )
            cls.cursor = cls.connection.cursor()

    @classmethod
    def get_last_id_wall(cls):
        DB.cursor.execute('SELECT id_wall FROM tWall')
        ids = DB.cursor.fetchall()
        return ids[-1]['id_wall']

    @classmethod
    def new_wall(cls):
        DB.cursor.execute('''INSERT INTO tWall (id_wall) VALUE (null)''')
        DB.connection.commit()
        return cls.get_last_id_wall()

    @classmethod
    def new_user(cls, name, city, img_path, visibility=3):
        if not os.path.isfile(img_path):
            img_path = 'users/user0.jpg'

        img_blob = imagem_blob(img_path)
        id_wall = cls.new_wall()

        DB.cursor.execute('INSERT INTO tUser (name, city, id_wall, visibility, image) VALUES (%s, %s, %s, %s, %s)', (name, city, id_wall, visibility, img_blob))
        DB.connection.commit()

    @classmethod
    def new_group(cls, name, description, img_path, visibility=1):
        if not os.path.isfile(img_path):
            img_path = 'groups/group0.jpg'

        img_blob = imagem_blob(img_path)
        id_wall = cls.new_wall()

        DB.cursor.execute('INSERT INTO tGroup (name, description, id_wall, visibility, image) VALUES (%s, %s, %s, %s, %s)', (name, description, id_wall, visibility, img_blob))
        DB.connection.commit()

        # Retornar id do grupo criado
        DB.cursor.execute('SELECT id_group FROM tGroup')
        ids = DB.cursor.fetchall()
        return ids[-1]['id_group']
