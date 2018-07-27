import keyboard, sys, os
from bin.splash import Splash
from .user_requests import Menus

class UserInterface:
    def __init__(self, user_requests):
        self.user_requests = user_requests

    menu_width = 77
    menu_border = 4  # including margin
    disconnected = False
    lines_printed = 0
    option_index = 0
    MENU_OPTIONS = 6
    system_exit_requested = False

    def print_title(self, title):
        spaces = ((self.menu_width - self.menu_border - len(title)) / 2) * ' '
        title_row = "  |"+spaces+title+spaces+"|"
        print ("  ,_________________________________________________________________________,")
        print ("  |                                                                         |")
        print (title_row)
        print ("  |_________________________________________________________________________|")
        print ("  |                                                                         |")

    def print_item(self, menu, item, index):
        if menu.selected == item:  # currently selected
            value = "  |   C==>  " + str(index) + ". " + item.text
        else:
            value = "  |         " + str(index) + ". " + item.text
        spaces = (self.menu_width - len(value) - 1) * ' '  # - 1 for ending border bracket, "|"
        print (value + spaces + '|')

    def print_menu(self, menu):
        Menus.open_menu = menu
        self.print_title(menu.title)
        index = 1
        for item in menu.items:
            self.print_item(menu, item, index)
            index = index + 1
        print ("  |_________________________________________________________________________|")

    def redraw_main_menu(self):
        os.system("cls")
        Splash.print_splash_screen()
        self.print_menu(Menus.main_menu)

    def call_back_yo(self, keybord_event):
        # Up key
        if self.disconnected:
            pass
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
        Splash.print_splash_screen()
        self.print_menu(Menus.main_menu)
        self.disconnected = False
        keyboard.on_press_key('up', self.call_back_yo)
        keyboard.on_press_key('down', self.call_back_yo)
        keyboard.on_press_key('enter', self.call_back_yo)

    def disconnect(self):
        self.disconnected = True
