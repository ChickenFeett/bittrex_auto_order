import keyboard
import sys
import os
import threading
from bin.splash import Splash
from .menus import Menus

class UserInterface:
    def __init__(self, menus):
        keyboard.on_press_key('up', self.call_back_yo)
        keyboard.on_press_key('down', self.call_back_yo)
        keyboard.on_press_key('enter', self.call_back_yo)
        self.menus = menus

    menu_width = 77
    menu_border = 4  # including margin
    disconnected = False
    lines_printed = 0
    MENU_OPTIONS = 6
    system_exit_requested = False

    def print_title(self, title):
        spaces = int((self.menu_width - self.menu_border - len(title)) / 2) * ' '
        title_row = "  |"+spaces+title+spaces+"|"
        print ("  ,_________________________________________________________________________,")
        print ("  |                                                                         |")
        print (title_row)
        print ("  |_________________________________________________________________________|")
        print ("  |                                                                         |")

    def print_item(self, menu, item, index):
        if menu.selected == item.index:  # currently selected
            value = "  |   C==>  " + str(index) + ". " + item.text
        else:
            value = "  |         " + str(index) + ". " + item.text
        spaces = int(self.menu_width - len(value) - 1) * ' '  # - 1 for ending border bracket, "|"
        print (value + spaces + '|')

    def print_menu(self, menu):
        Menus.open_menu = menu
        self.print_title(menu.title)
        index = 1
        for key, item in menu.items.items():
            # due to two keys mapped to one item, only process one of the keys types
            if type(key) is int:
                self.print_item(menu, item, index)
                index = index + 1
        print ("  |_________________________________________________________________________|")

    def redraw_main_menu(self):
        self.redraw(self.menus.main_menu)

    def call_back_yo(self, keybord_event):
        # Up key
        if self.disconnected:
            return
        lock = threading.Lock()
        if not lock.acquire(False):  # attempt non-blocking lock
            return  # already processing
        if keybord_event.scan_code == 72:
            if self.menus.current_menu.selected > 0:
                self.menus.current_menu.selected = self.menus.current_menu.selected - 1
                self.redraw_main_menu()
        # Down key
        if keybord_event.scan_code == 80:
            if self.menus.current_menu.selected < len(self.menus.current_menu.items)/2 - 1:
                self.menus.current_menu.selected = self.menus.current_menu.selected + 1
                self.redraw_main_menu()
        # Down key
        if keybord_event.scan_code == 28:
            self.menus.current_menu.items[self.menus.current_menu.selected].is_activated = True
        lock.release()  # release lock

    def run(self):
        self.redraw(self.menus.main_menu)
        self.disconnected = False

    def redraw(self, menu):
        lock = threading.Lock()
        if lock.acquire(False):  # attempt non-blocking lock
            os.system("cls")
            Splash.print_splash_screen()
            self.print_menu(menu)
            lock.release()  # release lock

    def disconnect(self):
        self.disconnected = True
