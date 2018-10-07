import keyboard
import msvcrt
import os
import threading
from bin.splash import Splash
from .menus import Menus
from .configuration import LoggingModes
from utils import Utils
import Queue


class UserInterface:
    def __init__(self, menus, fatal_exception_callback):
        keyboard.on_press_key('up', self.handle_key_press)
        keyboard.on_press_key('down', self.handle_key_press)
        keyboard.on_press_key('enter', self.handle_key_press)
        self.menus = menus
        self.current_menu = menus.current_menu
        self.handle_fatal_exception = fatal_exception_callback

    callback_queue = Queue.Queue()
    menu_width = 77
    menu_border = 4  # including margin
    disconnected = False
    lines_printed = 0
    MENU_OPTIONS = 6
    system_exit_requested = False

    def print_title(self, title):
        title = self.format_title(title)
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
            callback = None
            if self.disconnected:
                return
            if self.current_menu is None:
                return
            lock = threading.Lock()
            if not lock.acquire(False):  # attempt non-blocking lock
                return  # already processing
            # Up key
            if keybord_event.scan_code == 72:
                if self.current_menu.selected > 0:
                    self.current_menu.selected = self.current_menu.selected - 1
                    self.draw(self.current_menu)
            # Down key
            if keybord_event.scan_code == 80:
                if self.current_menu.selected < len(self.current_menu.items)/2 - 1:
                    self.current_menu.selected = self.current_menu.selected + 1
                    self.draw(self.current_menu)
            # Enter key
            if keybord_event.scan_code == 28:
                callback = self.current_menu.items[self.current_menu.selected].callback
                self.disconnect()
            lock.release()  # release lock
            if callback is not None:
                self.callback_queue.put(callback)
        except Exception, ex:
            self.handle_fatal_exception(ex)

    def run(self, menu):
        Utils.log("Running menu " + menu.title, LoggingModes.DEBUG)
        self.draw(menu)
        self.connect(menu)

    def draw(self, menu):
        lock = threading.Lock()
        if lock.acquire(False):  # attempt non-blocking lock
            os.system("cls")
            Splash.print_splash_screen()
            self.print_menu(menu)
            lock.release()  # release lock

    def disconnect(self):
        self.disconnected = True
        self.current_menu = None

    def connect(self, menu):
        self.current_menu = menu
        self.disconnected = False

    def wait_for_any_key(self, return_menu):
        while msvcrt.kbhit():
            msvcrt.getch()  # remove any key presses on the buffer first
        raw_input("Press enter to continue...")  # then wait for key to arrive
        self.run(return_menu)

    # Format title to present in GUI by adding spaces between each character.
    #  E.G. "My Title" -> "M  Y     T  I  T  L  E"
    @staticmethod
    def format_title(title):
        formatted_title = ""
        for x in range(0, len(title) - 2):  # for each character, excluding last character
            # create title format with two spaces separating each char
            formatted_title = formatted_title + title[x] + "  "
        return formatted_title + title[len(title)-1]  # add last character

