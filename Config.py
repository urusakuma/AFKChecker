from collections import namedtuple
from os import path
import configparser
from os.path import expanduser

def create_constant_from_ini():
    config_ini_path = "./AFKChecker.ini"
    Config = namedtuple(
        "Config",
        [
            # AFKと判断する間隔。デフォルトで1時間半。
            "AFK_INTERVAL",
            # AFKの確認頻度。デフォルトで10秒。
            "FREQUENCY_TO_CHECK_AFK",
            # 起きていると判断するクリックの回数。デフォルトで2回。
            "NUMBER_OF_TIMES_CLICK",
            # クリックを一度に行ったと判断する制限時間。デフォルトで60秒。
            "CLICK_TIME_LIMIT",
            # 起きていると判断するスクロールの回数。ホイールを半回転させた絶対値の合計は6ぐらい。デフォルトで4回。
            "NUMBER_OF_TIMES_SCROLL",
            # スクロールを一度に行ったと判断する制限時間。デフォルトで10秒。
            "SCROLL_TIME_LIMIT",
            # CSVファイルのパス。デフォルトで~\Desktop\AFK_Log.csv
            "LOG_FILE_PATH",
        ],
    )  
    if not path.exists(config_ini_path):
        # 指定したiniファイルが存在しない場合、Noneを返す。
        intervals = type("ReturnNone", (object,), {"getint": lambda e: None})
        awakening = type("ReturnNone", (object,), {"getint": lambda e: None})
        csv_path = type("ReturnNone", (object,), {"get": lambda e: None})
    else:
        # 指定したiniファイルが存在する場合、intervals、config_pathをiniファイルから読み取る。
        config_ini = configparser.ConfigParser()
        config_ini.read(config_ini_path, encoding="utf-8")
        intervals = config_ini["INTERVAL"]
        awakening = config_ini["AWAKENING"]
        csv_path = config_ini["PATH"]
        del config_ini

    const = Config(
        intervals.getint("AFK_INTERVAL") or 90 * 60,
        intervals.getint("FREQUENCY_TO_CHECK_AFK") or 10,
        intervals.getint("NUMBER_OF_TIMES_CLICK") or 2,
        intervals.getint("CLICK_TIME_LIMIT") or 60,
        awakening.getint("NUMBER_OF_TIMES_SCROLL") or 4,
        awakening.getint("SCROLL_TIME_LIMIT") or 10,
        csv_path.get("LOG_FILE_PATH") or expanduser("~\\Desktop\\AFK_Log.csv"),
    )
    del config_ini_path, intervals, awakening, csv_path
    return const

CONFIG = create_constant_from_ini()
del create_constant_from_ini
