from tkinter import *
from database import *
from random import choice


class RecordableListbox(Listbox):
    def __init__(self, listname: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__recorder = ListRecorder(listname)
        self.__rewrite_content()
        
    def __rewrite_content(self):
        self.delete(0, END)
        self.insert(END, *self.__recorder.get_content())

    def change_listsave(self, new_listname: str, save_current: bool = True):
        self.__recorder.change_listsave(new_listname, save_current)
        self.__rewrite_content()

    def append(self, elem: str):
        self.insert(END, elem)
        self.__recorder.append(elem)

    def remove(self) -> bool:
        cursel = self.curselection()
        good = bool(cursel)

        if good:
            index: int = cursel[0]
            self.delete(index)
            self.__recorder.delete(index)

        return good

    def clear(self):
        self.delete(0, END)
        self.__recorder.clear()

    def choose(self) -> str | None:
        lst = self.__recorder.get_content()
        if len(lst) > 0: return choice(lst)
