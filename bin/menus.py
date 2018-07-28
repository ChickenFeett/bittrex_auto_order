class Menus:
    def __init__(self):
        self.main_menu = self.Menu(
            1,
            "M  A  I  N     M  E  N  U",
            [
                self.Menu.MenuItem(0, "Print Open Orders"),
                self.Menu.MenuItem(1, "Print Balances"),
                self.Menu.MenuItem(2, "Place Orders"),
                self.Menu.MenuItem(3, "Configuration"),
                self.Menu.MenuItem(4, "Exit")
            ],
        )

        self.configuration = self.Menu(
            2,
            "C  O  N  F  I  G  U  R  A  T  I  O  N",
            [
                self.Menu.MenuItem(0, "Enter API Key"),
                self.Menu.MenuItem(1, "Print API Key"),
                self.Menu.MenuItem(2, "Enter Secret Key"),
                self.Menu.MenuItem(3, "Print Secret Key")
            ]
        )

        self.current_menu = self.main_menu


    class Menu:
        def __init__(self, index, title, items):
            self.index = index
            self.title = title
            self.selected = 0
            self.items = {}
            for item in items:
                self.items[item.text] = item
                self.items[item.index] = item

        class MenuItem:
            def __init__(self, index, text):
                self.index = index
                self.text = text
                self.is_activated = False



