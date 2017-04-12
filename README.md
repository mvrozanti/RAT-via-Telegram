# RAT-via-Telegram

Windows Remote Administration Tool via Telegram

### Why another one?

The current Remote Administration Tools in the market face 2 major problems:

- Lack of encryption
- Require port forwarding in order to control from hundreds of miles

This RAT overcomes both these issues by using the Telegram bot API.

- Fully encrypted. The data being exchanged cannot be spied upon using MITM tools
- Telegram messenger app provides a simple way to communicate to the target without configuring port forward before hand on the target

## Features:

- Run keylogger on the target PC
- Get target PC's Windows version, processor and more.
- List any directories on the target.
- Download any file locally from the target PC in the background.
- Upload local files on to the target PC. Just send any file to the Telegram bot that you wish to upload.
- Screenshots of the target PC.
- Take snapshots from the webcam (if attached).
- Self-Destruct RAT with a single command.
- Many more coming soon!

## Screenshots:

## Installation & Usage:

- Set up a new Telegram bot talking to the BotFather.
- Copy the token and add it in the bottom of the script.
- Clone this repository.
- Install dependencies: `pip install -r requirements.txt`
- To run the script: `python TeleRAT.py`
- Send messages to the bot!

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
