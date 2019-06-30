# RAT-via-Telegram
[![Build Status](https://travis-ci.org/mvrozanti/RAT-via-Telegram.svg?branch=master)](https://travis-ci.org/mvrozanti/RAT-via-Telegram)
[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3572A5.svg)](https://travis-ci.org/mvrozanti/RAT-via-Telegram)

Windows Remote Administration Tool via Telegram (now in Python 3.7!) | Originally created by <a href="http://github.com/Ritiek">Ritiek</a>

### Why another one?

- The current Remote Administration Tools in the market face 2 major problems:

    - Lack of encryption.
    - Require port forwarding in order to control from hundreds of miles.

- This RAT overcomes both these issues by using the Telegram bot API.

    - Fully encrypted. The data being exchanged cannot be spied upon using MITM tools.
    - Telegram messenger app provides a simple way to communicate to the target without configuring port forward before hand on the target.

## Features:

- Keylogger with window title log included
- Get target PC's Windows version, processor and more
- Get target PC's IP address information and approximate location on map
- Delete, Move files
- Show current directory
- Change current directory
- List current or specified directory
- Download any file from the target
- Upload local files to the target. Send your image, pdf, exe or anything as `file` to the Telegram bot
- Autostart playing a video in fullscreen and no controls for a youtube video on target
- Take Screenshots
- Execute any file
- Access to microphone
- Start HTTP Proxy Server
- Freeze target's keyboard
- Schedule tasks to run at specified datetime
- Encode/Decode all local files
- Ping targets
- Update .exe -- thanks <a href="http://github.com/LearnerZone">LearnerZone</a>
- Self-Destruct RAT
- Change wallpaper from file or url
- Execute cmd shell
- Take snapshots from the webcam (if attached)
- Execute arbitrary python 3.7 on the go
- Freeze target's mouse
- [TODO] Browser (IE, Firefox, ~~Chrome~~) cookies retrieval
- [TODO] Password retrieval
- [TODO] Monitor web traffic (graphically?)
- [TODO] Bandwidth monitoring (stepping stone to web traffic monitoring) - started 28/10/2018
- [TODO] Fine-tuning scripting (i.e.: if app x is opened y is executed)
- [TODO] Capture clipboard (Text, Image)
- [TODO] Hide desktop icons
- [TODO] Audio compression
- [TODO] Name server lookup (/nslookup - <a href="https://github.com/mvrozanti/RAT-via-Telegram/issues/19">#19</a>)

 Thanks <a href="http://github.com/Dviros">Dviros</a>:
- Chrome login/password retrieval
- Display ARP table
- Get active processes and services
- Shutdown/Reboot computer
- Display DNS Cache


& More coming soon!

## Screenshots:

<img src="http://i.imgur.com/I5nzrbz.jpg"/>

## Installation & Usage:

- Clone this repository.
- Set up a new Telegram bot talking to the `BotFather`.
- Copy this token and replace it in the beginning of the script.
- Run `compile.py`
  - Generates an executable binary
- To run the script: `python RATAttack.py`.
- Find your bot on telegram and send some command to the bot to test it.
- To restrict the bot so that it responds only to you, note down your `chat_id` from the console and replace it in the script and comment out the line `return True`. Don't worry, you'll know when you read the comments in the script.

<img src="http://i.imgur.com/XKARtrp.png">

- A folder named `RATAttack` will be created in your working directory containing `keylogs.txt` and any files you upload to the bot.

### Commands:

When using the below commands; use `/` as a prefix. For example: `/pc_info`.

```
arp - display arp table
capture_pc - screenshot PC
cmd_exec - execute shell command
cp - copy files
cd - change current directory
delete - delete a file/folder
download - download file from target
decode_all - decode ALL encoded local files
dns - display DNS Cache
encode_all - encode ALL local files
freeze_keyboard - enable keyboard freeze
unfreeze_keyboard - disable keyboard freeze
get_chrome - Get Google Chrome's login/passwords
hear - record microphone
ip_info - via ipinfo.io
keylogs - get keylogs
ls - list contents of current or specified directory
msg_box - display message box with text
mv - move files
pc_info - PC information
ping - makes sure target is up
play - plays a youtube video
proxy - opens a proxy server
pwd - show current directory
python_exec - interpret python
reboot - reboot computer
run - run a file
schedule - schedule a command to run at specific time
self_destruct - destroy all traces
shutdown - shutdown computer
tasklist - display services and processes running
to - select targets by it's name
update - update executable
wallpaper - change wallpaper
```

You can copy the above to update your command list via `BotFather` so you don't have to type them manually.

## Compiling:

### How To Compile:
- Run `compile.py`. You can also pass `--icon=<path/to/icon.ico>` to use a custom icon. If you want to use UPX for compression, you can add `--upx-dir [upx-3.95-win64 | upx-3.96-win32]`, depending on your architecture. You can skip this last option if you have UPX in your `PATH` environment variable.
- Once it is compiled successfully, find the `.exe` file in `C:/Python37/Scripts/dist/` or the current directory, depending on where you called it from.
- **BEWARE!** If you run the compiled `.exe`, the script will move itself to startup and start with your PC to run at startup. You can return to normal by using the `/self_destruct` option or manually removing `%APPDATA%/Portal` directory and `%APPDATA%/Microsoft/Windows/Start Menu/Programs/Startup/portal.lnk`.

### Modifying Settings:

- You can also modify the name of hidden `.exe` file and location and name of the folder where the hidden `.exe` will hide itself. To do this; modify `compiled_name` and `hide_folder` respectively.
- Assign your known chat ids to beginning of RATAttack.py

## Contributing:

- This project is still in very early stages, so you can expect some bugs. Please feel free to report them! Even better, send a pull request :)
- Any new features and ideas are most welcome! Please do submit feature requests by creating Issues
- Branch protection is enabled on `master`. You must work in an alternate branch (e.g. `dev`) and make a PR. This is to ensure that master has a working and approved version of RvT.

## Credit
A markdown file with credits:
 <a href="https://github.com/mvrozanti/RAT-via-Telegram/blob/master/CREDIT.md">Credit file</a>

People with PRs:
 - <a href="https://gituhb.com/dudeisbrendan03">Brendan | some stuff</a>
 - <a href="http://github.com/Dviros">Dviros | Chrome login/password retrieval | ARP Table | Process/services | shutdown/reboot | dns cache</a>
 - <a href="http://github.com/LearnerZone">LearnerZone | Support on updating the executable</a>

Dependency owners:
 <a href="https://github.com/mvrozanti/RAT-via-Telegram/network/dependencies">A load of people who turn coffee to code</a>

Original creator:
 - <a href="http://github.com/Ritiek">Ritiek | Original RAT dev</a>

## Disclaimer:

**This tool is supposed to be used only on authorized systems. Any unauthorized use of this tool without explicit permission is illegal.**

## License:

`The MIT License`
