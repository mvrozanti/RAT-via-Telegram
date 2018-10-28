#Files are sourced from https://www.lfd.uci.edu/~gohlke/pythonlibs/, disclaimer from site below
"""
The files are unofficial (meaning: informal, unrecognized, personal, unsupported, no warranty, no liability, provided "as is") and made available for testing and evaluation purposes.

Most binaries are built from source code found on PyPI or in the projects public revision control systems. Source code changes, if any, have been submitted to the project maintainers or are included in the packages.

Refer to the documentation of the individual packages for license restrictions and dependencies.

If downloads fail, reload this page, enable JavaScript, disable download managers, disable proxies, clear cache, use Firefox, reduce number and frequency of downloads. Please only download files manually as needed.

Use pip version 9 or newer to install the downloaded .whl files. This page is not a pip package index.

Many binaries depend on numpy-1.14+mkl and the Microsoft Visual C++ 2008 (x64, x86, and SP1 for CPython 2.7), Visual C++ 2010 (x64, x86, for CPython 3.4), or the Visual C++ 2017 (x64 or x86 for CPython 3.5, 3.6, and 3.7) redistributable packages.

Install numpy+mkl before other packages that depend on it.

The binaries are compatible with the most recent official CPython distributions on Windows >=6.0. Chances are they do not work with custom Python distributions included with Blender, Maya, ArcGIS, OSGeo4W, ABAQUS, Cygwin, Pythonxy, Canopy, EPD, Anaconda, WinPython etc. Many binaries are not compatible with Windows XP or Wine.

The packages are ZIP or 7z files, which allows for manual or scripted installation or repackaging of the content.

The files are provided "as is" without warranty or support of any kind. The entire risk as to the quality and performance is with you."""
#This script will compare hashes to make sure that they are valid and original from the server
#Items we need imported most of the time
import hashlib
import re
import urllib.request
import os

#Functions
def validHash(hash):#MD5 Verifier
    vHash = re.finditer(r'(?=(\b[A-Fa-f0-9]{32}\b))', hash)
    result = [match.group(1) for match in validHash]
    if result:  return True
    else:   return False

def genHash(item):
    hash_md5 = hashlib.md5()
    with open(item, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def validate(hash,source):
    urllib.request.urlretrieve(source, 'temp.whl')
    newHash = genHash('temp.whl')
    if hash == newHash: print("OK")
    elif hash != newHash: raise Exception('CHECKSUM DID NOT "CHECK" OUT, IT IS INVALID. MAKE SURE THAT YOUR VERSION HAS NOT BEEN ALTERED, OR THE SOURCE HAS NOT BEEN ALTERED')
    os.remove('temp.whl')


#pyAudio
#amd64
currentHash = genHash('PyAudio-0.2.11-cp37-cp37m-win_amd64.whl')
validHash(currentHash)
validate(currentHash,'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/pyHook-1.5.1-cp37-cp37m-win_amd64.whl')
#win32
currentHash = genHash('PyAudio-0.2.11-cp37-cp37m-win32.whl')
validHash(currentHash)
validate(currentHash,'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/PyAudio-0.2.11-cp37-cp37m-win32.whl')

#pyHook
#amd64
currentHash = genHash('pyHook-1.5.1-cp37-cp37m-win_amd64.whl')
validHash(currentHash)
validate(currentHash,'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/pyHook-1.5.1-cp37-cp37m-win_amd64.whl')
#win32
currentHash = genHash('pyHook-1.5.1-cp37-cp37m-win32.whl')
validHash(currentHash)
validate(currentHash,'https://download.lfd.uci.edu/pythonlibs/h2ufg7oq/pyHook-1.5.1-cp37-cp37m-win32.whl')