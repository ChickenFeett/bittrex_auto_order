import sys
import requests
from bin.splash import splash
from bin.utilities import utilities

EXPECTED_API_KEY_LENGTH = 32

class bittrex_orderer:
	def __init__(self):
		print "Initializing"

	def read_api_key(self):
		f = open('api_key', 'r')
		contents = f.read()
		if len(contents) != EXPECTED_API_KEY_LENGTH:
			print "Warning: API Key is not in the expected format. Key: " + str(contents) + " with length of: " + str(len(contents))
		return contents

	def login(self):
		# Atempt to login
		print "Attempting to login"

splash.print_splash_screen()

b_orderer = bittrex_orderer()
api_key = b_orderer.read_api_key()
api_key = utilities.read_orders_from_file()
if not b_orderer.login():
	print "Login failed. Please retry."
	sys.exit()

print "Login success."