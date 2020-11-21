##########################################################################################
#   忘れ物防止アラート: ルーティング設定とAPI処理内容を定義します。
##########################################################################################
import sqlite3
import configparser
from datetime import datetime as dt


# 定数定義
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WAITSEC_AFTER_PUT = 5.0
INVALID_ID = 2

# 設定ファイル読み込み
config = configparser.ConfigParser()
config.read("status/settings.ini")

# データベース設定
DBPATH = config["has_item"]["path"]
DBTABLE = config["has_item"]["table"]
DEFAULTID = config["has_item"]["defaultid"]
DEFAULTNAME = config["has_item"]["defaultname"]
conn = sqlite3.connect(DBPATH)


@get("/status/has_item/reset")
def reset():
	"""諸々初期化
	"""
	cursor = conn.cursor()
	cursor.execute("DROP TABLE IF EXISTS %s" % DBTABLE)
	cursor.execute("CREATE TABLE IF NOT EXISTS %s (id INTEGER PRIMARY KEY, name TEXT, value int, last_put_time TEXT)" % DBTABLE)
	cursor.execute(
		"INSERT INTO %s VALUES (?, ?, ?, ?)" % DBTABLE,
		(DEFAULTID, DEFAULTNAME, 0, dt.now().strftime(DATETIME_FORMAT))
	)
	conn.commit()
	return {}


@post("/status/has_item/get")
def get():
	"""所持フラグを立てます。
	"""
	cursor = conn.cursor()
	cursor.execute(
		"UPDATE %s SET value = ? WHERE name = ?" % DBTABLE,
		(1, DEFAULTNAME)
	)
	conn.commit()
	return {}


@post("/status/has_item/put")
def put():
	"""所持フラグを解除します。
	"""
	cursor = conn.cursor()
	cursor.execute(
		"UPDATE %s SET value = ?, last_put_time = ? WHERE name = ?" % DBTABLE,
		(0, dt.now().strftime(DATETIME_FORMAT), DEFAULTNAME)
	)
	conn.commit()
	return {}


@post("/status/has_item/check")
def check():
	"""所持したかどうかを確認します。
	"""
	cursor = conn.cursor()
	cursor.execute(
		"SELECT value, strftime(last_put_time) FROM %s WHERE name = ?" % DBTABLE,
		(DEFAULTNAME,)
	)
	result = cursor.fetchone()

	if result is None:
		return {
			"result": -1,
		}
	else:
		# if result[0] == 1 and (dt.now() - dt.strptime(result[1], DATETIME_FORMAT)).total_seconds() < WAITSEC_AFTER_PUT:
		# 	# 所持していない場合、最後に置いたときから一定時間経っていないと無効にする: アナログGPIO入力が過敏に反応するのを回避するため
		# 	result = [INVALID_ID]

		return {
			"result": result[0],
		}
