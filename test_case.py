from redesocial.database import DB
from redesocial.utils import imagem_blob, ver_imagem
import sys
import os
from PIL import Image

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

DB()

table = 'tTest'
user_pic_path = 'users/'
group_pic_path = 'groups/'


def drop_tables():
    # Do not change the order
    tables = [
        'rUser_User',
        'rUser_Wall',
        'rGroup_Wall',
        'rUser_Group',
        'tReply',
        'tComment',
        'tPost',
        'tGroup',
        'tUser',
        'tWall',
    ]

    for table in tables:
        DB.cursor.execute(f'DROP TABLE IF EXISTS {table}')


def create_tables():
    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tWall(
        id_wall INTEGER NOT NULL AUTO_INCREMENT,
        PRIMARY KEY (id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tUser(
        id_user INTEGER NOT NULL AUTO_INCREMENT,
        id_wall INTEGER NOT NULL,
        visibility INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        city VARCHAR(255),
        image BLOB,
        PRIMARY KEY (id_user),
        FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tGroup(
        id_group INTEGER NOT NULL AUTO_INCREMENT,
        id_wall INTEGER NOT NULL,
        visibility INTEGER NOT NULL,
        name VARCHAR(255) NOT NULL,
        description VARCHAR(512),
        image BLOB,
        PRIMARY KEY (id_group),
        FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tPost(
        id_post INTEGER NOT NULL AUTO_INCREMENT,
        id_user INTEGER NOT NULL,
        id_wall INTEGER NOT NULL,
        text VARCHAR(512),
        image BLOB,
        PRIMARY KEY (id_post),
        FOREIGN KEY (id_user) REFERENCES tUser(id_user),
        FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tComment(
        id_comment INTEGER NOT NULL AUTO_INCREMENT,
        id_user INTEGER NOT NULL,
        id_post INTEGER NOT NULL,
        text VARCHAR(512) NOT NULL,
        PRIMARY KEY (id_comment),
        FOREIGN KEY (id_user) REFERENCES tUser(id_user),
        FOREIGN KEY (id_post) REFERENCES tPost(id_post)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS tReply(
        id_reply INTEGER NOT NULL AUTO_INCREMENT,
        id_user INTEGER NOT NULL,
        id_comment INTEGER NOT NULL,
        text VARCHAR(512) NOT NULL,
        PRIMARY KEY (id_reply),
        FOREIGN KEY (id_user) REFERENCES tUser(id_user),
        FOREIGN KEY (id_comment) REFERENCES tComment(id_comment)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS rUser_User(
        id_user_from INTEGER NOT NULL,
        id_user_to INTEGER NOT NULL,
        status INTEGER NOT NULL,
        PRIMARY KEY (id_user_from, id_user_to),
        FOREIGN KEY (id_user_from) REFERENCES tUser(id_user),
        FOREIGN KEY (id_user_to) REFERENCES tUser(id_user)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS rUser_Wall(
        id_user INTEGER NOT NULL,
        id_wall INTEGER NOT NULL,
        PRIMARY KEY (id_user, id_wall),
        FOREIGN KEY (id_user) REFERENCES tUser(id_user),
        FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS rGroup_Wall(
        id_group INTEGER NOT NULL,
        id_wall INTEGER NOT NULL,
        PRIMARY KEY (id_group, id_wall),
        FOREIGN KEY (id_group) REFERENCES tGroup(id_group),
        FOREIGN KEY (id_wall) REFERENCES tWall(id_wall)
    );''')

    DB.cursor.execute('''CREATE TABLE IF NOT EXISTS rUser_Group(
        id_user INTEGER NOT NULL,
        id_group INTEGER NOT NULL,
        status INTEGER NOT NULL,
        PRIMARY KEY (id_user, id_group),
        FOREIGN KEY (id_user) REFERENCES tUser(id_user),
        FOREIGN KEY (id_group) REFERENCES tGroup(id_group)
    );''')


def new_wall():
    DB.cursor.execute('''INSERT INTO tWall (id_wall) VALUE (null)''')
    DB.connection.commit()


global id_wall
id_wall = 1
global user_num
user_num = 1
global group_num
group_num = 1


def new_user(name, city, visibility=3, image='null'):
    global id_wall
    global user_num
    filepath = f'{user_pic_path}user{user_num}.jpg'
    if not os.path.isfile(filepath):
        filepath = f'{user_pic_path}user0.jpg'
    img_blob = imagem_blob(filepath)
    new_wall()
    DB.cursor.execute('INSERT INTO tUser (name, city, id_wall, visibility, image) VALUES (%s, %s, %s, %s, %s)', (name, city, id_wall, visibility, img_blob))
    DB.connection.commit()
    id_wall += 1


def new_group(name, description, visibility=1, image='null'):
    global id_wall
    global group_num
    filepath = f'{group_pic_path}group{group_num}.jpg'
    if not os.path.isfile(filepath):
        filepath = f'{group_pic_path}group0.jpg'
    img_blob = imagem_blob(filepath)
    new_wall()
    DB.cursor.execute('INSERT INTO tGroup (name, description, id_wall, visibility, image) VALUES (%s, %s, %s, %s, %s)', (name, description, id_wall, visibility, img_blob))
    DB.connection.commit()
    id_wall += 1


def populate_tables():
    new_user('Caio Moraes', 'João Pessoa')
    new_user('Samuel Moura', 'João Pessoa')
    new_user('Manuela Silva', 'Patos')
    new_user('Priscila Oliveira', 'Campina Grande')
    new_user('Raquel Nascimento', 'Guarabira')
    new_user('Daniel Cavalcanti', 'Patos')
    new_user('Pedro Belfort', 'João Pessoa')
    new_user('Luciana Souza', 'Campina Grande')

    new_group('UFPB', 'Grupo da UFPB')
    new_group('CI', 'Grupo do CI-UFPB')
    new_group('CT', 'Grupo do CT-UFPB')
    new_group('DEMID', 'Grupo do DEMID-UFPB')


drop_tables()
create_tables()
populate_tables()
# img_blob = imagem_blob("../users/user{0}.jpg".format(4))
# DB.cursor.execute(f'INSERT INTO {table} (img) VALUES (%s)', (img_blob,))
# DB.connection.commit()
# DB.cursor.execute(f'SELECT img FROM {table}')
# instance = DB.cursor.fetchone()
# ver_imagem(instance)
print('Schema populated')