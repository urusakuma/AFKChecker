from time import sleep
import mouse
import keyboard
from Config import CONFIG
from Logger import Logger
from UserInputTracker import UserInputTracker

logger          :Logger = Logger(CONFIG.LOG_FILE_PATH, CONFIG.AFK_INTERVAL)
mouse_click     :UserInputTracker = UserInputTracker(CONFIG.NUMBER_OF_TIMES_CLICK, CONFIG.CLICK_TIME_LIMIT, logger)
mouse_wheel     :UserInputTracker = UserInputTracker(CONFIG.NUMBER_OF_TIMES_SCROLL, CONFIG.SCROLL_TIME_LIMIT, logger)
keyboard_push   :UserInputTracker = UserInputTracker(1, 1,logger)
def handle_mouse_events(args):
    """マウスのイベントを取得する。

    Args:
        args (_type_): _description_
    """
    if isinstance(args, mouse.ButtonEvent):
        if args.event_type == "up":
            mouse_click.track_user_action()

    if isinstance(args, mouse.WheelEvent):
            mouse_click.track_user_action(abs(args.delta))


def handle_keyboard_events(args):
    """キーボードのイベントを取得する。
    Args:
        args (_type_): _description_
    """
    keyboard_push.track_user_action()

def main():
    # PCを操作していたなら最終操作時刻を更新するようにコールバック。
    keyboard.hook(handle_keyboard_events)
    mouse.hook(handle_mouse_events)
    FREQUENCY_TO_CHECK_AFK = CONFIG.FREQUENCY_TO_CHECK_AFK
    while True:
        sleep(FREQUENCY_TO_CHECK_AFK)
        if not logger.should_write():
             continue
        logger.postscript_nowDate()
        

if __name__ == "__main__":
    main()
