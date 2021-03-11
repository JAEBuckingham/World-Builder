"""character gui"""
import tkinter as tk


class Character(tk.Toplevel):
    """character gui window"""

    def __init__(self, master, character_id=None):
        tk.Toplevel.__init__(self, master)
        self.session = None
        self.title(f'character #{character_id}')
        self.config(background='light blue')
        self.name = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name)
        self.name_entry.grid(row=0, column=0)

        # name
        # description
        # relationships
        # goals
        # event history
        # location
        # likes
        # dislikes
        # fears
        # skills
        # knowledge
        # possessions
        # personality


if __name__ == '__main__':
    master = tk.Tk()
    test = Character(master, 'bob')
    master.mainloop()
