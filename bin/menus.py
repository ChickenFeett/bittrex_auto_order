from utils import Utils
from configuration import LoggingModes


class Menus:
    def __init__(self):
        Utils.log("Initializing Menus", LoggingModes.DEBUG)

        Utils.log("Creating Main Menu", LoggingModes.DEBUG)
        self.main_menu = self.Menu(
            1,
            "Main Menu",
            [
                self.Menu.MenuItem("Orders"),
                self.Menu.MenuItem("Configuration"),
                self.Menu.MenuItem("Exit")
            ],
        )

        Utils.log("Creating Orders Menu", LoggingModes.DEBUG)
        self.orders_menu = self.Menu(
            2,
            "Orders",
            [
                self.Menu.MenuItem("Print Open Orders"),
                self.Menu.MenuItem("Print Balances"),
                self.Menu.MenuItem("Place Orders"),
                self.Menu.MenuItem("Back")
            ],
        )

        Utils.log("Creating Configuration Menu", LoggingModes.DEBUG)
        self.configuration = self.Menu(
            3,
            "Configuration",
            [
                self.Menu.MenuItem("Enter New API Key"),
                self.Menu.MenuItem("Print API Key"),
                self.Menu.MenuItem("Enter New Secret Key"),
                self.Menu.MenuItem("Print Secret Key"),
                self.Menu.MenuItem("Back")
            ]
        )

        Utils.log("Setting default current menu ( Menu Main )", LoggingModes.DEBUG)
        self.current_menu = self.main_menu

    class Menu:
        def __init__(self, menu_id, title, items):
            self.menu_id = menu_id
            self.title = title
            self.selected = 0
            self.items = {}
            for index, item in enumerate(items):
                item.index = index
                self.items[item.text] = item
                self.items[item.index] = item

        class MenuItem:
            def __init__(self, text):
                self.index = None
                self.text = text
                self.callback = None



