import sys
import requests
from binna.splash import splash

class bittrex_orderer:
	def __init__(self, api_key):
		print "Initializing"

	def login(self):
		# Atempt to login
		print "Attempting to login"


splash.printSplashScreen()	


b_orderer = bittrex_orderer("api_key")
if not b_orderer.login():
	print "Login failed. Please retry."
	sys.exit()

print "Login success."





