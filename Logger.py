from time import time as now
from datetime import datetime
class Logger:
    LOG_FILE_PATH: str
    AFK_INTERVAL: int
    last_actioned_time: int
    penultimate_actioned_time: int
    def __init__(self, log_file_path: str, afk_interval: int):
        self.LOG_FILE_PATH = log_file_path
        self.AFK_INTERVAL = afk_interval
        self.last_actioned_time = now()
        self.penultimate_actioned_time = now()

    def record_now_time(self):
        """最終操作時刻を変更する。"""
        self.last_actioned_time = now()
    
    def postscript_nowDate(self):
        """textファイルに睡眠時刻を追記する。"""
        start_time = datetime.fromtimestamp(self.penultimate_actioned_time).strftime("%m/%d,%H:%M,") 
        end_time = datetime.now().strftime("%H:%M")
        self.penultimate_actioned_time = self.last_actioned_time
        with open(self.LOG_FILE_PATH, mode="a") as f:
            f.write(start_time + end_time + "\n")

    def is_afk(self, now_time, check_time:float) -> bool:
        """調べる時刻が一定時間を超えているか検出しTrueを返す。操作をしていたならFalseを返す。
        Parameters:
            check_time : float  最後に操作した時刻
        Returns:
            bool : しばらく操作をしていないならTrue、操作をしていたならFalse。
        """
        return self.AFK_INTERVAL < now_time - check_time

    def should_write(self)->bool:
        """睡眠時間を書き込むべきか判断する関数。書き込むべきならTrueを返す。
        Returns:
            bool: Trueなら睡眠時間を書き込むべき。Falseなら書き込むべきではない。
        """
        now_time = now()
        # 最直近で長い間操作していないなら起きていないのでFalse
        if self.is_afk(now_time, self.last_actioned_time):
            return False
        # 前回操作したのが規定時間より短ければ寝ていないので、最直近の時刻を書き換えてFalse
        if not self.is_afk(now_time, self.penultimate_actioned_time):
            self.penultimate_actioned_time = self.last_actioned_time
            return False
        return True