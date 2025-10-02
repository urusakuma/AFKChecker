from datetime import datetime
from os.path import exists

def create_constant_from_ini():
    from collections import namedtuple
    from os import path
    import configparser
    from os.path import expanduser

    config_ini_path = "./SleepStopWatch.ini"
    Config = namedtuple(
        "Config",
        [
            # CSVファイルのパス。デフォルトで~\Desktop\AFK_Log.csv
            "CSV_FILE_PATH",
        ],
    )  
    if not path.exists(config_ini_path):
        # 指定したiniファイルが存在しない場合、Noneを返す。
        csv_path = type("ReturnNone", (object,), {"get": lambda e: None})
    else:
        # 指定したiniファイルが存在する場合、intervals、config_pathをiniファイルから読み取る。
        config_ini = configparser.ConfigParser()
        config_ini.read(config_ini_path, encoding="utf-8")
        csv_path = config_ini["PATH"]
        del config_ini
    
    const = Config(
        csv_path.get("CSV_FILE_PATH") or expanduser("~\\Desktop\\AFK_Log.csv"),
    )
    del config_ini_path, csv_path
    return const
CONFIG = create_constant_from_ini()
del create_constant_from_ini


def postscript_text(contents: str):
    """
    textファイルに追記する。
    Parameters
    ----------
    contents
        textファイルに追記する内容。
    """
    with open(CONFIG.CSV_FILE_PATH, mode="a") as f:
        f.write(contents)
def is_end_of_file_afk() -> bool:
    """
    最後に記録されたのがAFKか確認する。AFKから復帰した場合とAFKを記録していない場合はFalse、AFKの記録のみがある場合はTrue
    Returns
    -------
    bool : 最後に記録されているのがAFKならTrue、それ以外ならFalse(正確には最後が\n以外ならTrue)
    """
    if not exists(CONFIG.CSV_FILE_PATH):  # AFKLogが存在しない。
        return False
    with open(CONFIG.CSV_FILE_PATH, mode="r") as f:
        s = f.read()
        if s.__len__() == 0:  # AFKLogが空
            return False
        return "\n" != s[-1]  # AFKLogの最後が\nか。

def main():
    if not is_end_of_file_afk() :
        # AFKになった時刻を追記。
        postscript_text(datetime.now().strftime("%m/%d,%H:%M,"))
    else :
        # AFKから復帰した時刻を追記。
        postscript_text(datetime.now().strftime("%H:%M") + "\n")
if __name__ == "__main__":
    main()