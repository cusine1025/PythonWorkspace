import sqlite3
from assets.parameter import *

class DataBase:
    def __init__(self,tableName,**options) -> None:
        self.tableName = tableName
        self.option = options
        tableSet = ', '.join(map(lambda x: f'{x} {options[x]}',options.keys()))

        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        #tableExist = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        #if table doesn't exist
        #if not any(map(lambda x : x[0] == tableName,tableExist)):
        cur.execute(f'''CREATE TABLE IF NOT EXISTS {tableName} (id INTEGER PRIMARY KEY AUTOINCREMENT, {tableSet})''')
        con.commit()
        con.close()
    
    def add(self,value):
        self.excute(f'''INSERT INTO {self.tableName} {tuple(self.option.keys())} VALUES {tuple(value)}''')
    
    def fetchall(self):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        result = cur.execute(f'''SELECT * FROM {self.tableName}''').fetchall()
        con.commit()
        con.close()
        return result
    
    def select(self,condition):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        result = cur.execute(f'''SELECT * FROM {self.tableName} WHERE {condition}''').fetchall()
        con.commit()
        con.close()
        return result
    
    def update(self,condition,col,value):
        self.excute(f'''UPDATE {self.tableName} SET '{col}' = '{value}' WHERE {condition};''')
    
    def IscolExist(self,colName):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        result = cur.execute(f'''PRAGMA table_info({self.tableName});''').fetchall()
        if any(map(lambda x:x[1] == colName,result)):
            result = True
        else:
            result = False
        con.commit()
        con.close()
        return result
    
    def addCol(self,name,typeOfCol):
        self.excute(f'ALTER TABLE {self.tableName} ADD COLUMN \'{name}\' {typeOfCol};')
    
    def excute(self,command):
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        cur.execute(command)
        con.commit()
        con.close()
    
    @staticmethod
    def getTableInfo():
        con = sqlite3.connect(DATABASE_PATH)
        cur = con.cursor()
        result = cur.execute(f"SELECT name FROM sqlite_master WHERE type='table';").fetchall()
        result = [list(map(lambda x:x[0],result)),[]]
        for table in result[0]:
            result[1].append(cur.execute(f'PRAGMA table_info({table});').fetchall())
        con.commit()
        con.close()
        return dict([(result[0][i],result[1][i]) for i in range(len(result[0]))])