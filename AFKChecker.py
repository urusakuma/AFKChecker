from os.path import exists
from time import sleep, time as now
import mouse
import keyboard
from datetime import datetime
from os import getenv, path
import configparser

config_ini_path = "AFKChecker.ini"
# 指定したiniファイルが存在しない場合、Noneを返却するクラスを作成する。
if not path.exists(config_ini_path):
    class ReturnNone:
        pass

    intervals = ReturnNone()
    config_path = ReturnNone()
    setattr(intervals, "getint", lambda x: None)
    setattr(config_path, "get", lambda x: None)
    del ReturnNone
else:
    config_ini = configparser.ConfigParser()
    config_ini.read(config_ini_path, encoding='utf-8')
    intervals = config_ini["INTERVAL"]
    config_path = config_ini["PATH"]
    del config_ini

# AFKと判断する間隔。デフォルトで1時間半。
AFK_INTERVAL = intervals.getint("AFK_INTERVAL") or 90 * 60
# AFKでないことを確認した後、AFKか確認することを止める時間。デフォルトで10分。
COOLING_PERIOD_AFTER_CHECK_AFK = intervals.getint("COOLING_PERIOD_AFTER_CHECK_AFK") or 10 * 60
# AFKの確認頻度。デフォルトで10秒。
FREQUENCY_TO_CHECK_AFK = intervals.getint("FREQUENCY_TO_CHECK_AFK") or 10

# CSVファイルのパス。デフォルトで"HOMEDRIVE""HOMEPATH"\Desktop\AFK_Log.csv
CSV_FILE_PATH = config_path.get("CSV_FILE_PATH") or \
                getenv("HOMEDRIVE") + getenv("HOMEPATH") + "\\Desktop\\AFK_Log.csv"
del config_ini_path, intervals, config_path

# 最後に操作したunix時刻。
last_moved_time: float = now()


def is_afk(last_time: float) -> bool:
    """
    一定時間操作をしていないことを検出しTrueを返す。操作をしていたならFalseを返す。
    Parameters
    ----------
    last_time : float
        最後に操作した時刻
    Returns
    -------
    bool : しばらく操作をしていないならTrue、操作をしていたならFalse。
    """
    return AFK_INTERVAL < now() - last_time


def postscript_text(contents: str):
    """
    textファイルに追記する。
    Parameters
    ----------
    contents
        textファイルに追記する内容。
    """
    with open(CSV_FILE_PATH, mode="a") as f:
        f.write(contents)


def put_now_time_in_global(e):
    """
    呼び出された時の時刻をグローバル変数に代入する。
    """
    global last_moved_time
    last_moved_time = e.time


def is_end_of_file_afk() -> bool:
    """
    最後に記録されたのがAFKか確認する。AFKから復帰した場合とAFKを記録していない場合はFalse、AFKの記録のみがある場合はTrue
    Returns
    -------
    bool : 最後に記録されているのがAFKならTrue、それ以外ならFalse(正確には最後が\n以外ならTrue)
    """
    if not exists(CSV_FILE_PATH):  # AFKLogが存在しない。
        return False
    with open(CSV_FILE_PATH, mode="r") as f:
        return "\n" != f.read()[-1]


def main():
    # 起動時にAFKで途切れていたか。
    is_before_check_afk = is_end_of_file_afk()

    # PCを操作していたなら最終操作時刻を更新するようにコールバック。マウスの移動はAFKからの復帰とみなさない。
    keyboard.on_press(lambda e: put_now_time_in_global(e))
    mouse.hook(lambda e: put_now_time_in_global(e) if mouse.MoveEvent != type(e) else 0)

    while True:
        sleep(FREQUENCY_TO_CHECK_AFK)
        # AFKではないか確認する。
        if not is_afk(last_moved_time):
            # AFKから復帰したか確認する。
            if is_before_check_afk:
                # AFKから復帰したなら時刻を追記。
                postscript_text(datetime.now().strftime(",%H:%M") + "\n")
                is_before_check_afk = False

            sleep(COOLING_PERIOD_AFTER_CHECK_AFK)
            continue
        # 既にAFKなら追記しない。
        if is_before_check_afk:
            continue
        # 新たにAFKになったならログを追記。
        postscript_text(datetime.fromtimestamp(last_moved_time).strftime("%m/%d,%H:%M"))
        is_before_check_afk = True


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:  # 強制終了された。WinのKillコマンドではこの例外は機能しない。
        if is_afk(last_moved_time):  # AFKの場合、AFKの時刻を書き込む。
            postscript_text(datetime.fromtimestamp(last_moved_time).strftime("%m/%d,%H:%M"))
        # 例外を外に投げる。
        raise KeyboardInterrupt
