import pymysql


class DB:
    connection = None
    cursor = None

    @classmethod
    def __init__(self):
        if self.connection is None or self.cursor is None:
            self.connection = pymysql.connect(
                host='127.0.0.1',
                db='myface_schema',
                user='myfaceAdm',
                password='myfaceAdm',
                cursorclass=pymysql.cursors.DictCursor
            )
            self.cursor = self.connection.cursor()
