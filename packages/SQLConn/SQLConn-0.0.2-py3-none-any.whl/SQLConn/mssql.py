from SQLConn import SQLConn
import pymssql
class MSSQLConn(SQLConn):
    def __init__(self,host:str='127.0.0.1',user:str="sa",password:str=None,database:str="master",port:str|int=1433) -> None:
        super.__init__()
        self.__host=host
        self.__user=user
        self.__password=password
        self.__database=database
        self.__port=int(port)
        self._conn=pymssql.connect(host=self.__host,user=self.__user,password=self.__password,database=self.__database,port=self.__port)
        self._engine=self._makeEngine()
    @property
    def URL(self):
        return f'mssql+pyodbc://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}'