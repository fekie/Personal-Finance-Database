import sqlite3
import json

global config
with open("config.json") as f:
  config = json.load(f)

con = sqlite3.connect("../databases/db_v" + config["DbVersion"] + "/db_v" + config["DbVersion"] + ".db")
cur = con.cursor()

#cur.execute()
con.commit()

con.close()