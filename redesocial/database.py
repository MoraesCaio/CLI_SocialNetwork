import pymysql


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
