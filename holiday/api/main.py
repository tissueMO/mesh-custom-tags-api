##########################################################################################
#    祝日を含む休日を判定するAPIです。
##########################################################################################
from datetime import datetime
from datetime import date
import jpholiday
import json


# 定数定義
DATE_FORMAT = "%Y/%m/%d"
WEEKDAYS = {
    "月": 0,
    "火": 1,
    "水": 2,
    "木": 3,
    "金": 4,
    "土": 5,
    "日": 6,
}


def is_holiday(request):
    """指定された日付が休日であるかどうかを返します。

    Arguments:
      request: HTTPリクエストデータ
    Returns:
      {bool} -- 土日祝のいずれかに当てはまる場合はTrueを返します。
    """
    if not "date" in request:
        return ("date要素がありません", 400, None)

    try:
        dt = datetime.strptime(request["date"], DATE_FORMAT)
        dt = date(dt.year, dt.month, dt.day)
    except:
        return ("日付は yyyy/mm/dd の形式の文字列にして下さい", 400, None)

    result = {
        "is_holiday": _is_holiday(dt),
    }

    return (json.dumps(result), 200, None)


def _is_holiday(dt: date) -> bool:
    """休日であるかどうかを返します。

    Arguments:
      dt {date} -- 対象の日付
    Returns:
      {bool} -- 土日祝のいずれかに当てはまる場合はTrueを返します。
    """
    if dt.weekday() in [WEEKDAYS["土"], WEEKDAYS["日"]]:
        return True
    elif jpholiday.is_holiday(dt):
        return True
    else:
        return False
