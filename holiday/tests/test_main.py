##########################################################################################
#    祝日を含む休日を判定するAPIのテストコードです。
##########################################################################################
import api.main as main
from datetime import date
import pytest


@pytest.mark.parametrize("year, month, day, expected", [
    # 平日
    (2018, 5, 1, 0),
    # 土曜日
    (2020, 11, 21, 1),
    # 日曜日
    (2020, 11, 22, 1),
    # 祝日
    (2020, 11, 23, 1),
    # 平成天皇誕生日
    (2018, 12, 23, 1),
    # 平成における平日の令和天皇誕生日
    (2018, 2, 23, 0),
    # 令和天皇誕生日
    (2021, 2, 23, 1),
    # 令和における平日の平成天皇誕生日
    (2021, 12, 23, 0),
])
def test_is_holiday(year: int, month: int, day: int, expected: int):
    assert main._is_holiday(date(year, month, day)) == expected
