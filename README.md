AFKChecker
====
目的・解決した課題
対象ユーザ
アプリを作成した動機
使用言語
使用ライブラリ・フレームワークなど
開発環境
主な機能
工夫した点
実装に苦労した部分と解決方法
成果
今後追加したい機能
改善点や学びたい技術
Detects AFK and falling asleep. Then logged the time.
Logged if you do not operate the keyboard, not click the mouse, or not operate the wheel. 
It also log the time when you returned from AFK.

AFKや寝落ちを検出し、時刻を記録します。
キーボードの操作やマウスのクリック、ホイールの操作を行わないなら記録します。
AFKから復帰した時刻も記録します。

## Warning
**It works like a keylogger. Be sure to check for danger.**
**Please let me know if you find a problem.**

**キーロガーの様に動作します。危険ではないか必ず調べてください。**
**問題を見つけたら教えてください。**

## Usage
You can adjust the time to judge AFK in AFKChecker.ini.
You can also set the log storage location. 

AFKChecker.iniでAFKと判断する時間やログの保存場所などを調整できます。

## Installation
1. Click Code in the upper right corner. Get AFKChecker.py and AFKChecker.ini. 
2. Use PyInstaller to convert it to an exe file. 
```
   python -m pip install pyinstaller
   pyinstaller AFKChecker.py --onefile --noconsole
```
3. Register for StartUp.

All you have to do is sleep. 

1. 右上にあるCodeをクリックしてAFKChecker.pyとAFKChecker.iniを取得してください。
2. PyInstallerを使用してexeファイルに変換します。
```
   python -m pip install pyinstaller
   pyinstaller AFKChecker.py --onefile --noconsole
```
3. スタートアップに登録します。

あとは寝落ちるだけです。
