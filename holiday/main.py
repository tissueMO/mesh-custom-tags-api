##########################################################################################
#    祝日を含む休日を判定するAPIです。
##########################################################################################
from datetime import date
import jpholiday


# 定数定義
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
