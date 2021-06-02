import os
import sqlite3
import time
import math
from datetime import datetime

class db:
    
    def __init__(self, directory, version, assetTypeList):
        if not os.path.exists(directory + "/db_v" + version):
            os.makedirs(directory + "/db_v" + version)
                
        self.Connection = sqlite3.connect(directory + "/db_v" + version + "/db_v" + version + ".db")
        self.Cursor = self.Connection.cursor()
        
        
        self.Cursor.execute("CREATE TABLE IF NOT EXISTS balance (asset_type TEXT PRIMARY KEY, amount FLOAT, last_time_string TEXT, last_time_unix INTEGER)")
        
        for type in assetTypeList:
            self.Cursor.execute("INSERT OR IGNORE INTO balance (asset_type, amount, last_time_string, last_time_unix) VALUES (?, ?, ?, ?)", (type, 0.0, datetime.today().strftime('%m-%d-%Y||%H:%M:%S'), int(time.time())))
        self.Connection.commit()