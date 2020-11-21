##########################################################################################
#   天気情報を取得するAPIです。
##########################################################################################
from datetime import datetime as dt
from bs4 import BeautifulSoup
from statistics import mean
import requests
import os
import codecs
import json

# 設定値ロード
import configparser
config = configparser.ConfigParser()
config.read("./config.ini", "UTF-8")

WEATHER_SOURCE_URL = config.get("weather", "weather_source_url")
WARNING_SOURCE_URL = config.get("weather", "warning_source_url")
INVALID_CELL = config.get("weather", "invalid_cell")
TARGET_TIME_INDICES = list(json.loads(config.get("weather", "target_time_indices")))
TARGET_WARNINGS = list(json.loads(config.get("weather", "target_warnings")))
DATETIME_FORMAT = config.get("weather", "datetime_format")
VALID_CACHE_MINUTES = int(config.get("weather", "valid_cache_minutes"))
CACHE_WEATHER_FILE = config.get("weather", "cache_weather_file")
CACHE_WARNING_FILE = config.get("weather", "cache_warning_file")


def check() -> int:
    """雨傘チェッカー

    Returns:
      int -- 危険度 1-5 or 判定不能 -1
    """
    try:
        level = _get_rain_level()
        is_warn = _has_warn()
    except Exception as e:
        import traceback
        traceback.print_exec()
        return {
            "result": -1
        }

    if level == 4 and is_warn:
        # 警報付きの場合にLv.MAX
        level = 5

    return {
        "result": level
    }


def _has_cache_weather() -> bool:
    """直前の天気データを持つHTMLを流用できるかどうかを調べます。

    Returns:
      bool -- 直前の天気データを持つHTMLを流用できる場合はTrue、それ以外はFalse
    """
    if not os.path.exists(CACHE_WEATHER_FILE):
        # まだ実行されていない
        return False

    with codecs.open(CACHE_WEATHER_FILE, "r", encoding="UTF-8") as fweather:
        last_time_str = fweather.readline().replace("\n", "")
        last_time = dt.strptime(last_time_str, DATETIME_FORMAT)
        now_time = dt.now()
        delta = now_time - last_time

        if VALID_CACHE_MINUTES < delta.total_seconds() / 60:
            # 有効期間を過ぎている
            print("_has_cache_weather: 有効期間切れ")
            return False

    return True


def _load_cache_weather() -> str:
    """直前の天気データを持つHTMLを読み込みます。

    Returns:
      str -- 直前の天気データを持つHTML
    """
    if not os.path.exists(CACHE_WEATHER_FILE):
        # まだ実行されていない
        return False

    with codecs.open(CACHE_WEATHER_FILE, "r", encoding="UTF-8") as fweather:
        fweather.readline()
        return fweather.read()


def _save_cache_weather(html: str):
    """最後に取得した天気データを持つHTMLを書き出します。

    Arguments:
      html {str} -- 天気データを持つHTML
    """
    with codecs.open(CACHE_WEATHER_FILE, "w", encoding="UTF-8") as fweather:
        # 現在時刻を埋め込み
        fweather.write(dt.now().strftime(DATETIME_FORMAT) + "\n")

        # 実際のHTMLは2行目から
        fweather.write(html)

    os.chmod(CACHE_WEATHER_FILE, 0o0600)


def _has_cache_warning() -> bool:
    """直前の警報データを持つHTMLを流用できるかどうかを調べます。

    Returns:
      bool -- 直前の警報データを持つHTMLを流用できる場合はTrue、それ以外はFalse
    """
    if not os.path.exists(CACHE_WARNING_FILE):
        # まだ実行されていない
        return False

    with codecs.open(CACHE_WARNING_FILE, "r", encoding="UTF-8") as fwarning:
        last_time_str = fwarning.readline().replace("\n", "")
        last_time = dt.strptime(last_time_str, DATETIME_FORMAT)
        now_time = dt.now()
        delta = now_time - last_time

        if VALID_CACHE_MINUTES < delta.total_seconds() / 60:
            # 有効期間を過ぎている
            print("_has_cache_warning: 有効期間切れ")
            return False

    return True


def _load_cache_warning() -> str:
    """直前の警報データを持つHTMLを読み込みます。

    Returns:
      str -- 直前の警報データを持つHTML
    """
    if not os.path.exists(CACHE_WARNING_FILE):
        # まだ実行されていない
        return False

    with codecs.open(CACHE_WARNING_FILE, "r", encoding="UTF-8") as fwarning:
        fwarning.readline()
        return fwarning.read()


def _save_cache_warning(html: str):
    """最後に取得した警報データを持つHTMLを書き出します。

    Arguments:
      html {str} -- 警報データを持つHTML
    """
    with codecs.open(CACHE_WARNING_FILE, "w", encoding="UTF-8") as fwarning:
        # 現在時刻を埋め込み
        fwarning.write(dt.now().strftime(DATETIME_FORMAT) + "\n")

        # 実際のHTMLは2行目から
        fwarning.write(html)

    os.chmod(CACHE_WARNING_FILE, 0o0600)


def _get_rain_level() -> int:
    """天気および降水確率から危険度を4段階で返します。

    Raises:
      Exception: レスポンスが正常に返ってこなかった場合に送出する

    Returns:
      int -- 危険度
        4: 雨を66%以上含む or 降水確率の平均が60%を超える
        3: 雨を含む or 降水確率の平均が40%を超える
        2: 曇りを含む or 降水確率の平均が0%を超える
        1: 晴れを含む or 降水確率の平均が0%
        -1: 翌日の予報まで過ぎてしまっているイレギュラーなケース。判定不能
    """
    # 天気情報取得
    has_cache = _has_cache_weather()
    if not has_cache:
        print("Non-Cache: " + WEATHER_SOURCE_URL)
        with requests.request("GET", WEATHER_SOURCE_URL) as response:
            if response.status_code != 200:
                raise Exception(
                    "天気予報サイトのレスポンスで200以外のステータスが返されました: " + response.status_code)
            html = response.text
    else:
        print("Cache: 天気HTMLロード")
        html = _load_cache_weather()

    for day_of_prob in ["forecast-point-1h-today", "forecast-point-1h-tomorrow"]:
        # 天気データをパース
        soup = BeautifulSoup(html, "html.parser")

        # 降水確率
        td_list_chance_of_rain = soup \
            .find("table", id=day_of_prob) \
            .find("tr", class_="prob-precip") \
            .find_all("td")
        target_chances_of_rain_every_one_hour = [
            y.text
            for i, y in enumerate([
                x.find("span") for x in td_list_chance_of_rain
            ])
            if i in TARGET_TIME_INDICES
        ]

        # 過ぎ去りし予報は除外
        target_chances_of_rain_every_one_hour = [
            int(x)
            for x in target_chances_of_rain_every_one_hour
            if x != INVALID_CELL and x.isdecimal()
        ]
        if len(target_chances_of_rain_every_one_hour) == 0:
            # すべて時刻が過去になっている場合は翌日にする
            print("明日の天気を判定します...")
            continue

        # 降水確率の平均値を出す
        chance_of_rain_mean = mean(target_chances_of_rain_every_one_hour)

        # 天気
        td_list_weather = soup \
            .find("table", id=day_of_prob) \
            .find("tr", class_="weather") \
            .find_all("td")
        target_weather_probs_list = [
            y.text
            for i, y in enumerate([
                x.find("p") for x in td_list_weather
            ])
            if i in TARGET_TIME_INDICES
        ]
        target_weather_probs = "".join(target_weather_probs_list)
        rain_count = target_weather_probs.count("雨")
        cloudy_count = target_weather_probs.count("曇")
        sunny_count = target_weather_probs.count("晴")
        print("降水確率平均: " + str(chance_of_rain_mean))
        print("雨の個数: " + str(rain_count))
        print("曇の個数: " + str(cloudy_count))
        print("晴の個数: " + str(sunny_count))

        if not has_cache:
            # キャッシュ書き出し
            _save_cache_weather(html)

        # 最終判定
        if len(TARGET_TIME_INDICES) * 2 / 3 <= rain_count or 60 <= chance_of_rain_mean:
            return 4
        elif 0 < rain_count or 40 <= chance_of_rain_mean:
            return 3
        elif 0 < cloudy_count or 0 < chance_of_rain_mean:
            return 2
        elif 0 < sunny_count or 0 == chance_of_rain_mean:
            return 1

    return -1


def _has_warn() -> bool:
    """雨に関する警報/特別警報が発表されているかどうかを判定します
    ただし、この情報は取得時点で発表されている情報です。

    Raises:
      Exception: レスポンスが正常に返ってこなかった場合に送出する

    Returns:
      bool -- 雨に関する警報/特別警報が発表されている場合はTrue、それ以外はFalse
    """
    has_cache = _has_cache_warning()
    if not has_cache:
        print("Non-Cache: " + WARNING_SOURCE_URL)
        with requests.request("GET", WARNING_SOURCE_URL) as response:
            if response.status_code != 200:
                raise Exception(
                    "天気予報サイト（注意報・警報）のレスポンスで200以外のステータスが返されました: " + response.status_code)
            html = response.text
    else:
        print("Cache: 警報HTMLロード")
        html = _load_cache_warning()

    # 警報データをパース
    soup = BeautifulSoup(html, "html.parser")
    warning_list_container = soup \
        .find("div", class_="map-warn-point-recent-entry")
    if warning_list_container is None:
        return False
    warning_list_span = warning_list_container \
        .find_all("span")
    warning_list = [x.text for x in warning_list_span]

    if not has_cache:
        # キャッシュ書き出し
        _save_cache_warning(html)

    # 最終判定
    for warn in warning_list:
        if warn in TARGET_WARNINGS:
            return True

    return False
