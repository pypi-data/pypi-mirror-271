from pandas import read_sql
import warnings
import cx_Oracle
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from abc import ABC, abstractmethod
import MySQLdb
import pymssql
import psycopg2
import sqlite3

class SQLConn(ABC):
    _engine:Engine
    def __init__(self):
        warnings.filterwarnings('ignore', category=DeprecationWarning)
    def __del__(self)->None:
        if self._conn:
            self._conn.close()
        if self._engine:
            self._engine.dispose()
    def _makeEngine(self):
        return create_engine(self.URL)
    @property
    @abstractmethod
    def URL(self)->str:
        pass
    @property
    def engine(self):
        return self.engine
    def to_DataFrame(self,cmd:str):
        if not (cmd.lower().startswith('select') or cmd.lower().startswith('show')):
            raise ValueError("to_DataFrame does only supports 'select' or 'show' commands.")
        return read_sql(cmd,self._conn)

    def execute(self,cmd:str):
        if cmd.lower().startswith('select'):
            raise ValueError("execute does not support 'select' operations. Use 'to_DataFrame' method for queries.")
        if cmd.lower().startswith('show'):
            raise ValueError("execute does not support 'show' operations. Use 'to_DataFrame' method for queries.")
        try:
            cur=self._conn.cursor()
            cur.execute(cmd)
            self._conn.commit()
        except Exception as e:
            warnings.warn(str(e))

    def to_csv(self, cmd:str, file_name:str,encoding:str="utf-8"):
        try:
            self.to_DataFrame(cmd).to_csv(file_name+".csv", index=False,encoding=encoding)
        except Exception as e:
            warnings.warn(str(e))

    def to_excel(self, cmd:str, file_name:str):
        try:
            self.to_DataFrame(cmd).to_excel(file_name+".xlsx", index=False)
        except Exception as e:
            warnings.warn(str(e))

    def to_tsv(self, cmd:str, file_name:str,encoding:str="utf-8"):
        try:
            self.to_DataFrame(cmd).to_csv(file_name+".tsv", sep="\t",index=False,encoding=encoding)
        except Exception as e:
            warnings.warn(str(e))
    def to_sql(self,cmd:str,name:str,other):
        if not (cmd.lower().startswith('select') or cmd.lower().startswith('show')):
            raise ValueError("to_sql does only supports 'select' or 'show' commands.")
        try:
            self.to_DataFrame(cmd).to_sql(name,other.engine.connect(),index=False,if_exists="replace")
        except Exception as e:
            warnings.warn(str(e))
class MYSQLConn(SQLConn):
    def __init__(self,password:str,host:str='127.0.0.1',user:str="root",database:str="mysql",port:str|int=3306) -> None:
        super.__init__()
        self.__host=host
        self.__user=user
        self.__password=password
        self.__database=database
        self.__port=int(port)
        self._conn=MySQLdb.connect(host=self.__host,user=self.__user,password=self.__password,database=self.__database,port=self.__port)
        self._engine=self._makeEngine()
    @property
    def URL(self):
        return f'mysql+mysqldb://{self.__user}:{self.__password}@{self.__host}:{self.__port}/{self.__database}'
class MSSQLConn(SQLConn):
    def __init__(self,password:str,host:str='127.0.0.1',user:str="sa",database:str="master",port:str|int=1433) -> None:
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
class OracleConn(SQLConn):
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
class SQLiteConn(SQLConn):
    def __init__(self,file_path:str) -> None:
        super.__init__()
        self.__file_path=file_path
        self._conn=sqlite3.connect(file_path)
        self._engine=self._makeEngine()
    @property
    def URL(self):
        return f'sqlite://{self.__file_path}'