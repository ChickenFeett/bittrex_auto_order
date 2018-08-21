from utils import Utils
from configuration import Config, LoggingModes

class ConfigController:
    def update_api_key(self):
        api_key = raw_input("Enter API Key: ")
        if len(api_key) != Config.EXPECTED_API_KEY_LENGTH:
            Utils.log(
                "API Key is not in the expected format. Key: " + str(api_key) + " with length of: " + str(len(api_key)),
                LoggingModes.ALL)
        try:
            f = open('api_key', 'w+')
            f.write(api_key)
            Utils.log("API Key Saved!", LoggingModes.ALL)
        except:
            Utils.log("Failed to write API Key", LoggingModes.ALL)

    def view_api_key(self):
        try:
            f = open('api_key', 'r')
            print ("API Key: " + f.read())
        except:
            Utils.log("Failed to open API Key", LoggingModes.ALL)

    def update_secret_key(self):
        secret_key = raw_input("Enter Secret Key: ")
        if len(secret_key) != Config.EXPECTED_SECRET_KEY_LENGTH:
            Utils.log(
                "Secret Key is not in the expected format. Key: " + str(secret_key) + " with length of: " + str(len(secret_key)),
                LoggingModes.ALL)
        try:
            f = open('secret_key', 'w+')
            f.write(secret_key)
            Utils.log("Secret Key Saved!", LoggingModes.ALL)
        except:
            Utils.log("Failed to write Secret Key", LoggingModes.ALL)

    def view_secret_key(self):
        try:
            f = open('secret_key', 'r')
            print ("Secret key: : " + f.read())
        except:
            Utils.log("Failed to open Secret Key", LoggingModes.ALL)
