import os
import sqlite3
import time
import math
from prettytable import PrettyTable
from datetime import datetime
import sys

class db:
    Connection = None
    Cursor = None
    AssetTypes = None
    
    def __init__(self, directory, version, assetTypeList):
        if not os.path.exists(directory + "/db_v" + version):
            os.makedirs(directory + "/db_v" + version)
                
        self.Connection = sqlite3.connect(directory + "/db_v" + version + "/db_v" + version + ".db")
        self.Cursor = self.Connection.cursor()
        
        
        self.Cursor.execute("CREATE TABLE IF NOT EXISTS balance (asset_type TEXT PRIMARY KEY, amount FLOAT, last_time_string TEXT, last_time_unix INTEGER)")
        
        self.AssetTypes = assetTypeList
        for type in assetTypeList:
            self.Cursor.execute("INSERT OR IGNORE INTO balance (asset_type, amount, last_time_string, last_time_unix) VALUES (?, ?, ?, ?)", (type, 0.0, datetime.today().strftime('%m-%d-%Y'), int(time.time())))
        self.Cursor.execute("INSERT OR IGNORE INTO balance (asset_type, amount, last_time_string, last_time_unix) VALUES (?, ?, ?, ?)", ("Total", 0.0, datetime.today().strftime('%m-%d-%Y'), int(time.time())))
        self.Connection.commit()
    
    def WaitForCommand(self):
        commandList = [
            "Edit",
            "View",
            "Exit"
        ]
        outputStr = "Options: ("
        
        i = 0
        for command in commandList:
            i += 1
            outputStr = outputStr + "[" + str(i) + "]" + commandList[i-1]
            if i != len(commandList):
                outputStr = outputStr + ", "
            else:
                outputStr = outputStr + ")"
        
        while True:
            print(outputStr)
            commandIndex = input(">>> ")
            if commandIndex.isnumeric() and int(commandIndex) <= len(commandList) and int(commandIndex) > 0:
                return commandList[int(commandIndex) - 1]
            else:
                print("Please return a number associated with an option.")
    
    def ExecuteCommand(self, command):
        if command == "Edit":
            self.Edit()
        elif command == "View":
            self.View()
        elif command == "Exit":
            self.Exit()
    
    def Edit(self):
        outputStr = "Choose Asset: ("
        
        i = 0
        for name in self.AssetTypes:
            i += 1
            outputStr = outputStr + "[" + str(i) + "]" + self.AssetTypes[i-1]
            if i != len(self.AssetTypes):
                outputStr = outputStr + ", "
            else:
                outputStr = outputStr + ") "
        outputStr = outputStr + "[" + str(len(self.AssetTypes) + 1) + "]Go Back"
        
        asset = ""
        amount = 0
        while True:
            print(outputStr)
            commandIndex = input(">>> ")
            if commandIndex.isnumeric() and int(commandIndex) <= len(self.AssetTypes) + 1 and int(commandIndex) > 0:
                if int(commandIndex) <= len(self.AssetTypes):
                    asset = self.AssetTypes[int(commandIndex) - 1]
                    print("Old Amount: " + str(self.GetAmount(asset)))
                    while True:
                        newAmount = input("New Amount: ")
                        try:
                            amount = float(newAmount)
                            break
                        except ValueError:
                            print("Please enter a number.")
                    break
                else:
                    return 
            else:
                print("Please return a number associated with an option.")

        self.ChangeEntryTo(asset, amount)
    
    def View(self):
        self.Cursor.execute("SELECT * FROM balance")
        self.Connection.commit()
        rows = self.Cursor.fetchall()
        pt = PrettyTable()
        pt.field_names = ["Type", "Amount", "Date Recorded"]
        for row in rows:
            pt.add_row(row[0:3])
        print(pt)
    
    def Exit(self):
        self.Connection.close()
        sys.exit()    
    
    def GetAmount(self, asset):
        self.Cursor.execute(f"SELECT amount FROM balance WHERE asset_type=='{asset}'")
        return float(self.Cursor.fetchall()[0][0])
    
    def CorrectTotal(self):
        amountsList = [amount[0] for amount in self.Cursor.execute("SELECT amount FROM balance WHERE asset_type!='Total'")]
        totalAmount = 0.0
        for amount in amountsList:
            totalAmount += amount
        self.Cursor.execute("REPLACE INTO balance (asset_type, amount, last_time_string, last_time_unix) VALUES (?, ?, ?, ?)", ("Total", totalAmount, datetime.today().strftime('%m-%d-%Y'), int(time.time())))
    
    def ChangeEntryTo(self, name, amount):
        self.Cursor.execute("REPLACE INTO balance (asset_type, amount, last_time_string, last_time_unix) VALUES (?, ?, ?, ?)", (name, amount, datetime.today().strftime('%m-%d-%Y'), int(time.time())))
        self.CorrectTotal()
        print(f"{name} amount changed to: " + str(amount))
        self.Connection.commit()