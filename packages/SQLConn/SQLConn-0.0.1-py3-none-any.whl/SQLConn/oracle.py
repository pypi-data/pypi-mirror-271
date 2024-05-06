import cx_Oracle
from SQLconn import SQLconn
class OracleConn(SQLconn):
    def __init__(self,password:str,host:str='127.0.0.1',user:str="system",database:str="xe",port:str|int=1521) -> None:
        super.__init__()
        self.__host=host
        self.__user=user
        self.__password=password
        self.__database=database
        self.__port=int(port)
        self._conn=cx_Oracle.connect(self.__user,self.__password,f'{self.__host}:{self.__port}/{self.__database}')
        self._engine=self._makeEngine()
    @property
    def URL(self):
        return f'oracle+cx_oracle://{self.__user}:{self.__password}@{self.__host}:{self.__port}/?service_name={self.__database}'