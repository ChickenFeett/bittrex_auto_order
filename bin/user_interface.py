import keyboard, sys, os
import msvcrt
from bin.splash import Splash

class UserInterface:
    def __init__(self, user_requests):
        self.user_requests = user_requests

    lines_printed = 0
    option_index = 0
    MENU_OPTIONS = 6
    system_exit_requested = False

    def main_menu(self):
        if (self.option_index == 0):
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |   .-->  1. Read Orders From Bittrex                                     |")
            print ("   \_/      2. Read Orders From File                                        |")
            print ("   /        3. Enter Bittrex Command                                        |")
            print ("  |         4. Enter API Key                                                |")
            print ("  |         5. Enter Secret Key                                             |")
            print ("  |         6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        elif (self.option_index == 1):
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |         1. Read Orders From Bittrex                                     |")
            print ("   \_.--->  2. Read Orders From File                                        |")
            print ("   /        3. Enter Bittrex Command                                        |")
            print ("  |         4. Enter API Key                                                |")
            print ("  |         5. Enter Secret Key                                             |")
            print ("  |         6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        elif (self.option_index == 2):
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |         1. Read Orders From Bittrex                                     |")
            print ("   \_       2. Read Orders From File                                        |")
            print ("   / `--->  3. Enter Bittrex Command                                        |")
            print ("  |         4. Enter API Key                                                |")
            print ("  |         5. Enter Secret Key                                             |")
            print ("  |         6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        elif (self.option_index == 3):
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |         1. Read Orders From Bittrex                                     |")
            print ("   \_       2. Read Orders From File                                        |")
            print ("   / \      3. Enter Bittrex Command                                        |")
            print ("  |   `-->  4. Enter API Key                                                |")
            print ("  |         5. Enter Secret Key                                             |")
            print ("  |         6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        elif (self.option_index == 4):
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |         1. Read Orders From Bittrex                                     |")
            print ("   \_       2. Read Orders From File                                        |")
            print ("   / \      3. Enter Bittrex Command                                        |")
            print ("  |   \     4. Enter API Key                                                |")
            print ("  |    `->  5. Enter Secret Key                                             |")
            print ("  |         6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        else:
            print ("  ,_________________________________________________________________________,")
            print ("  |                                                                         |")
            print ("  |                        M  A  I  N     M  E  N  U                        |")
            print ("  |_________________________________________________________________________|")
            print ("  |                                                                         |")
            print ("  |         1. Read Orders From Bittrex                                     |")
            print ("   \        2. Read Orders From File                                        |")
            print ("   /\       3. Enter Bittrex Command                                        |")
            print ("  |  \      4. Enter API Key                                                |")
            print ("  |   \     5. Enter Secret Key                                             |")
            print ("  |    `->  6. Exit                                                         |")
            print ("  |_________________________________________________________________________|")
        self.lines_printed = 10

    def redraw_main_menu(self):
        os.system("cls")
        Splash.print_splash_screen()
        self.main_menu()

    def call_back_yo(self, keybord_event):
        # Up key
        if keybord_event.scan_code == 72:
            if self.option_index > 0:
                self.option_index = self.option_index - 1
                self.redraw_main_menu()
        # Down key
        if keybord_event.scan_code == 80:
            if self.option_index < self.MENU_OPTIONS - 1:
                self.option_index = self.option_index + 1
                self.redraw_main_menu()
        # Down key
        if keybord_event.scan_code == 28:
            if self.option_index == 0:  # read orders
                self.user_requests.look_up_open_orders = True
                pass
            elif self.option_index == 1:  # place orders
                pass
            elif self.option_index == 2:  # something
                pass
            elif self.option_index == 3:  # enter API key
                pass
            elif self.option_index == 4:  # enter secret key
                pass
            elif self.option_index == 5:  # enter secret key: # exit
                os.system("cls")
                print( "See you next time!")
                self.user_requests.system_exit = True

    def run(self):
        os.system("cls")
        #msvcrt.getch()
        Splash.print_splash_screen()
        self.main_menu()
        keyboard.on_press_key('up', self.call_back_yo)
        keyboard.on_press_key('down', self.call_back_yo)
        keyboard.on_press_key('enter', self.call_back_yo)
