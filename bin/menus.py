class Menus:
    def __init__(self):
        self.main_menu = self.Menu(
            1,
            "M  A  I  N     M  E  N  U",
            [
                self.Menu.MenuItem("Orders"),
                self.Menu.MenuItem("Configuration"),
                self.Menu.MenuItem("Exit")
            ],
        )
        self.orders_menu = self.Menu(
            2,
            "O   R   D   E   R   S",
            [
                self.Menu.MenuItem("Print Open Orders"),
                self.Menu.MenuItem("Print Balances"),
                self.Menu.MenuItem("Place Orders"),
                self.Menu.MenuItem("Back")
            ],
        )


        self.configuration = self.Menu(
            3,
            "C  O  N  F  I  G  U  R  A  T  I  O  N",
            [
                self.Menu.MenuItem("Enter New API Key"),
                self.Menu.MenuItem("Print API Key"),
                self.Menu.MenuItem("Enter New Secret Key"),
                self.Menu.MenuItem("Print Secret Key"),
                self.Menu.MenuItem("Back")
            ]
        )

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



