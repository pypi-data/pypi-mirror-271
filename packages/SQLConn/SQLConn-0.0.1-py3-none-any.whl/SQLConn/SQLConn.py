from pandas import read_sql
import warnings
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from abc import ABC, abstractmethod

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