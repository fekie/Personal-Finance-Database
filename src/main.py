import sqlite3
import json
import dbClass as dbClass

global config
with open("config.json") as f:
  config = json.load(f)

db = dbClass.db(config["DatabasesPath"], config["DbVersion"], config["AssetTypes"])

while True:
  command = db.WaitForCommand()
  db.ExecuteCommand(command)
