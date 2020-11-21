##########################################################################################
#   永続的に状態管理を行うAPIです。
##########################################################################################
import sqlite3
import json
from datetime import datetime as dt

# 定数定義
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# 設定値ロード
import configparser
config = configparser.ConfigParser()
config.read("./config.ini", "UTF-8")

DBPATH = config.get("status", "path")
DBTABLE = config.get("status", "table")
NAMES = json.loads(config.get("status", "names"))

def get_connection() -> sqlite3.Connection:
    """SQLコネクションを返します。

    Returns:
        sqlite3.Connection: コネクションオブジェクト
    """
    return sqlite3.connect(DBPATH)


def reset():
    """諸々初期化
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {DBTABLE}")
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {DBTABLE} (id INTEGER PRIMARY KEY, name TEXT, value int, updated TEXT)")

    for i, name in enumerate(NAMES):
        cursor.execute(
            f"INSERT INTO {DBTABLE} VALUES (?, ?, ?, ?)",
            (i, name, 0, dt.now().strftime(DATETIME_FORMAT))
        )

    conn.commit()
    return {}


def on(request):
    """フラグを立てます。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {DBTABLE} SET value = ?, updated = ? WHERE name = ?",
        (1, dt.now().strftime(DATETIME_FORMAT), request["name"])
    )
    conn.commit()
    return {}


def off(request):
    """フラグを解除します。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {DBTABLE} SET value = ?, updated = ? WHERE name = ?",
        (0, dt.now().strftime(DATETIME_FORMAT), request["name"])
    )
    conn.commit()
    return {}


def set(request):
    """任意のステータス値をセットします。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"UPDATE {DBTABLE} SET value = ?, updated = ? WHERE name = ?",
        (request["value"], dt.now().strftime(DATETIME_FORMAT), request["name"])
    )
    conn.commit()
    return {}


def get_status(request):
    """ステータスを確認します。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT value FROM {DBTABLE} WHERE name = ?",
        (request["name"],)
    )
    result = cursor.fetchone()

    if result is None:
        return {
            "result": -1,
        }
    else:
        return {
            "result": result[0],
        }


def get_latest(request):
    """最後に実行された時刻を返します。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT strftime(updated) FROM {DBTABLE} WHERE name = ?",
        (request["name"],)
    )
    result = cursor.fetchone()

    if result is None:
        return {
            "result": -1,
        }
    else:
        return {
            "result": result[0],
        }


def get_latest_span(request):
    """最後に実行された時刻と現在時刻の差分秒数を返します。

    Arguments:
        request: HTTPリクエストデータ
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT strftime(updated) FROM {DBTABLE} WHERE name = ?",
        (request["name"],)
    )
    result = cursor.fetchone()

    if result is None:
        return {
            "result": -1,
        }
    else:
        # 時刻差分を算出
        time_updated = dt.strptime(result[0], DATETIME_FORMAT)
        time_now = dt.now()
        time_delta = time_now - time_updated
        return {
            "result": time_delta.total_seconds(),
        }
