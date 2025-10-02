import Logger
from time import time as now
class UserInputTracker:
    ACTION_LIMIT: int           # 通知する操作回数の値。この数値を超えたら通知をする。
    ACTION_WAIT_TIME: int       # 操作が連続して行われたと判断する待機時間。
    logger: Logger              # ログを記録するクラス
    last_action_time: float     # 最後に操作したUNIX時間。
    action_counter: int = 0     # 操作された回数。
    def __init__(self, action_limit:int, action_wait_time:int, logger:Logger):
        self.ACTION_LIMIT       = action_limit
        self.ACTION_WAIT_TIME   = action_wait_time
        self.logger             = logger
        self.last_action_time   = now()

    def track_user_action(self, action_num:int=1):
        """操作したことを受け取り、ログの最終操作時刻を書き換える、
        Args:
            action_num (int): 操作した回数 Defaults to 1.
        """
        now_time = now()
        #　前回の操作から一定以上時間が経過している場合はカウンターを0にする。
        if now_time - self.last_action_time > self.ACTION_WAIT_TIME:
            self.action_counter = 0
        # 最後の操作時刻を現在時刻にしてカウンターを増やす。
        self.last_action_time = now_time
        self.action_counter += action_num
        # 操作回数が一定以上になったらログを記録する。
        if self.action_counter < self.ACTION_LIMIT:
            return
        self.logger.record_now_time()
