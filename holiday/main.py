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


def _is_holiday(dt):
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


def is_holiday(request):
	"""指定された日付が休日であるかどうかを返します。

	Arguments:
		request (flask.Request): HTTP request object.
	Returns:
		{bool} -- 土日祝のいずれかに当てはまる場合はTrueを返します。
	"""
	if request.method != "POST":
		return ("", 405, None)

	request_json = request.get_json()
	if not "date" in request_json:
		return ("date要素がありません", 400, None)

	try:
		dt = datetime.strptime(request_json["date"], DATE_FORMAT)
		dt = date(dt.year, dt.month, dt.day)
	except:
		return ("日付は yyyy/mm/dd の形式の文字列にして下さい", 400, None)

	result = {}
	if dt.weekday() in [WEEKDAYS["土"], WEEKDAYS["日"]]:
		result["is_holiday"] = True
	elif jpholiday.is_holiday(dt):
		result["is_holiday"] = True
	else:
		result["is_holiday"] = False

	return (json.dumps(result), 200, None)


@post("/holiday/check")
def check():
	"""現在の日付が土日祝であるかどうかを調べます。
	"""
	return {
		"result": 1 if _is_holiday(date.today()) else 0,
	}


@post("/holiday/test_holiday")
def test1():
	"""2018/05/01の日付が土日祝であるかどうかを調べます。
	"""
	return {
		"result": 1 if _is_holiday(date(2019, 1, 1)) else 0,
	}


@post("/holiday/test_saturday")
def test2():
	"""2019/01/12の日付が土日祝であるかどうかを調べます。
	"""
	return {
		"result": 1 if _is_holiday(date(2019, 1, 12)) else 0,
	}


@post("/holiday/test_sunday")
def test3():
	"""2019/01/13の日付が土日祝であるかどうかを調べます。
	"""
	return {
		"result": 1 if _is_holiday(date(2019, 1, 13)) else 0,
	}


@post("/holiday/test_weekday")
def test4():
	"""2019/01/10の日付が土日祝であるかどうかを調べます。
	"""
	return {
		"result": 1 if _is_holiday(date(2019, 1, 10)) else 0,
	}
