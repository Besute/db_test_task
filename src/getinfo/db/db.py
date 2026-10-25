import psycopg

class DB:
    def __init__(self, dbname, user, password, host, port):
        self.__dbname = dbname
        self.__user = user
        self.__password = password
        self.__host = host
        self.__port = port

    def connect(self):
        return psycopg.connect(
            dbname=self.__dbname,
            user=self.__user,
            password=self.__password,
            host=self.__host,
            port=self.__port,
        )
