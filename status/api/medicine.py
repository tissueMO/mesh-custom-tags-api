##########################################################################################
#   お薬アラート: ルーティング設定とAPI処理内容を定義します。
##########################################################################################
import sqlite3
import configparser


# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read("status/settings.ini")

# データベース設定
DBPATH = config["medicine"]["path"]
DBTABLE = config["medicine"]["table"]
DEFAULTID = config["medicine"]["defaultid"]
DEFAULTNAME = config["medicine"]["defaultname"]
conn = sqlite3.connect(DBPATH)


@get("/status/medicine/reset")
def reset():
	"""諸々初期化
	"""
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS %s" % DBTABLE)
	cursor.execute("CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY, name TEXT, value int)" % DBTABLE)
	cursor.execute("INSERT INTO %s VALUES (?, ?, ?)" % DBTABLE, (DEFAULTID, DEFAULTNAME, 0))
	conn.commit()
	return {}


@post("/status/medicine/report")
def report():
	"""服用フラグを立てます。
	"""
	cursor = conn.cursor()
	cursor.execute("UPDATE %s SET value = ? WHERE name = ?" % DBTABLE, (1, DEFAULTNAME))
	conn.commit()
	return {}


@post("/status/medicine/unreport")
def unreport():
	"""服用フラグを解除します。
	"""
	cursor = conn.cursor()
	cursor.execute("UPDATE %s SET value = ? WHERE name = ?" % DBTABLE, (0, DEFAULTNAME))
	conn.commit()
	return {}


@post("/status/medicine/check")
def check():
	"""服用したかどうかを確認します。
	"""
	cursor = conn.cursor()
	cursor.execute("SELECT value FROM %s WHERE name = ?" % DBTABLE, (DEFAULTNAME,))
	result = cursor.fetchone()
	if result is None:
		return {
			"result": -1,
		}
	else:
		return {
			"result": result[0],
		}
