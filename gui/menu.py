"""root gui"""
import tkinter as tk

from gui.character import Character
from sql.sql import character_list, DataBase
from tables.characters import Characters
from tables.events import Events
from tables.locations import Locations


def expand(container, x=None, x2=None, y=None, y2=None, weight=1):
    if x is not None:
        if x2 is None:
            x2 = x + 1
        for i in range(x, x2):
            container.grid_columnconfigure(i, weight=weight)
    if y is not None:
        if y2 is None:
            y2 = y + 1
        for i in range(y, y2):
            container.grid_rowconfigure(i, weight=weight)


class MainWindow(tk.Tk):
    """ the root window for the program """

    def __init__(self):
        tk.Tk.__init__(self)
        self.data_base = DataBase()
        self.menu_bar = MenuBar(self, self.data_base)
        self.config(menu=self.menu_bar, background='light blue')

        self.characters_list = ItemFrame(self, Characters, self.data_base)
        self.events_list = ItemFrame(self, Events, self.data_base)
        self.locations_list = ItemFrame(self, Locations, self.data_base)

        self.characters_list.grid(row=0, column=0, sticky='nesw')
        self.events_list.grid(row=0, column=1, sticky='nesw')
        self.locations_list.grid(row=0, column=2, sticky='nesw')
        expand(self, x=0, x2=3, y=0)
        self.mainloop()

    def refresh(self):
        self.characters_list.refresh()
        self.events_list.refresh()
        self.locations_list.refresh()


class MenuBar(tk.Menu):
    """ menu bar for the root window """

    def __init__(self, parent, data_base):
        tk.Menu.__init__(self, parent)
        self.file_menu = FileMenu(self, parent, data_base)
        self.add_cascade(label="File", menu=self.file_menu)


class FileMenu(tk.Menu):
    """ file option on the root menu bar """

    def __init__(self, menu_bar, parent, data_base):
        tk.Menu.__init__(self, menu_bar, tearoff=0)
        self.data_base = data_base
        self.parent = parent
        self.add_command(label="New", command=self.new_sqlite_connection)
        self.add_command(label="Open", command=self.open_sqlite_connection)
        self.add_command(label="Save", command=self.commit_sesion)

    def new_sqlite_connection(self):
        self.data_base.new_sqlite_connection()
        self.parent.refresh()

    def open_sqlite_connection(self):
        self.data_base.open_sqlite_connection()
        self.parent.refresh()

    def commit_sesion(self):
        self.data_base.commit()



class ItemScroll(tk.Frame):
    def __init__(self, parent, table, data_base):
        tk.Frame.__init__(self, parent)
        self.scrollbar = tk.Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='nesw')
        self.item_list = ItemList(self, table, data_base)
        self.item_list.grid(row=0, column=0, sticky='nesw')
        self.item_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.item_list.yview)
        expand(self, x=0, y=0)

    def refresh(self):
        self.item_list.refresh()


class ItemList(tk.Listbox):
    def __init__(self, parent, table, connection):
        tk.Listbox.__init__(self, parent)
        self.table = table
        self.connection = connection

    def refresh(self):
        self.delete(0, tk.END)
        for item in character_list(self.table, self.connection.session):
            self.insert(tk.END, item)


class ItemFrame(tk.Frame):
    def __init__(self, parent, table, data_base):
        tk.Frame.__init__(self, parent)
        self.table = table
        self.name_label = tk.Label(self, text=table.__tablename__)
        self.name_label.grid(row=0, column=0, sticky='nesw')
        self.item_list = ItemScroll(self, table, data_base)
        self.item_list.grid(row=1, column=0, sticky='nesw')
        self.controls = ListControls(self)
        self.controls.grid(row=2, column=0, sticky='nesw')
        expand(self, x=0, y=1)

    def refresh(self):
        self.item_list.refresh()


class ListControls(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.add_button = tk.Button(self, text='Add', command=self.blank_character_window)
        self.add_button.grid(row=1, column=0, sticky='nesw')
        self.open_button = tk.Button(self, text='Open', command=self.blank_character_window)
        self.open_button.grid(row=0, column=0, columnspan=2, sticky='nesw')
        self.delete_button = tk.Button(self, text='Delete')
        self.delete_button.grid(row=1, column=1, sticky='nesw')
        expand(self, x=0, x2=2, y=0)

    def blank_character_window(self):
        Character(self)


if __name__ == '__main__':
    MainWindow()
