import psycopg2
from SQLConn import SQLConn
class PostgresqlConn(SQLConn):
    def __init__(self,password:str,host:str='127.0.0.1',user:str="postgres",database:str="postgres",port:str|int=5432) -> None:
        super.__init__()
        self.__host=host
        self.__user=user
        self.__password=password
        self.__database=database
        self.__port=int(port)
        self._conn=psycopg2.connect(host=self.__host,user=self.__user,password=self.__password,database=self.__database,port=self.__port)
        self._engine=self._makeEngine()
    @property
    def URL(self):
        return f'postgresql://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}'