# use statically
class Menus:
    class Menu:
        def __init__(self, index, title, items):
            self.index = index
            self.title = title
            self.items = items
            self.selected = None

        class MenuItem:
            def __init__(self, index, text):
                self.index = index
                self.text = text
                self.is_selected = False
                self.is_activated = False

    current_menu = None

    main_menu = Menu(
        1,
        "M  A  I  N     M  E  N  U",
        [
            Menu.MenuItem(1, "Print Open Orders"),
            Menu.MenuItem(2, "Print Balances"),
            Menu.MenuItem(3, "Place Orders"),
            Menu.MenuItem(4, "Configuration"),
            Menu.MenuItem(5, "Exit")
        ],
    )

    configuration = Menu(
        2,
        "C  O  N  F  I  G  U  R  A  T  I  O  N",
        [
            Menu.MenuItem(1, "Enter API Key"),
            Menu.MenuItem(2, "Print API Key"),
            Menu.MenuItem(3, "Enter Secret Key"),
            Menu.MenuItem(4, "Print Secret Key")
        ]
    )

