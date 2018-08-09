import keyboard
import msvcrt
import os
import threading
from bin.splash import Splash
from .menus import Menus

class UserInterface:
    def __init__(self, menus, fatal_exception_callback):
        keyboard.on_press_key('up', self.handle_key_press)
        keyboard.on_press_key('down', self.handle_key_press)
        keyboard.on_press_key('enter', self.handle_key_press)
        self.menus = menus
        self.current_menu = menus.current_menu
        self.handle_fatal_exception = fatal_exception_callback

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

    def handle_key_press(self, keybord_event):
        try:
            # Up key
            if self.disconnected:
                return
            lock = threading.Lock()
            if not lock.acquire(False):  # attempt non-blocking lock
                return  # already processing
            if keybord_event.scan_code == 72:
                if self.current_menu.selected > 0:
                    self.current_menu.selected = self.current_menu.selected - 1
                    self.draw()
            # Down key
            if keybord_event.scan_code == 80:
                if self.current_menu.selected < len(self.current_menu.items)/2 - 1:
                    self.current_menu.selected = self.current_menu.selected + 1
                    self.draw()
            # Down key
            if keybord_event.scan_code == 28:
                self.current_menu.items[self.current_menu.selected].callback()
            lock.release()  # release lock
        except Exception, ex:
            self.handle_fatal_exception(ex)

    def run(self, menu):
        self.current_menu = menu
        self.draw()
        self.disconnected = False

    def draw(self):
        lock = threading.Lock()
        if lock.acquire(False):  # attempt non-blocking lock
            os.system("cls")
            Splash.print_splash_screen()
            self.print_menu(self.current_menu)
            lock.release()  # release lock

    def disconnect(self):
        self.disconnected = True

    def wait_for_any_key(self, return_menu):
        print("Press any key to continue...")
        while msvcrt.kbhit():  # remove any keys in buffer
            msvcrt.getch()
        msvcrt.getch()  # then wait for key press
        self.run(return_menu)