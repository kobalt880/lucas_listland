from widgets import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import *
from tkinter.ttk import Combobox
BACK_COL = '#d0d0d0'
FRONT_COL = '#eeeeee'

def error(mess: str): showerror('Ошибка', mess)
def warning(mess: str): showwarning('Внимание', mess)
def info(mess: str, title: str = 'Успешно'): showinfo(title, mess)


class MainFrame(Frame):
    def __init__(self, listname: str, *args, **kwargs):
        super().__init__(*args, background=FRONT_COL, **kwargs)
        self.__listname = listname
        self.__curr_destroyed = False

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__main_list = RecordableListbox(self.__listname, self)
        self.__append_button = Button(self, text='Добавить элем.', command=self.__append_lst)
        self.__delete_button = Button(self, text='Удалить элем.', command=self.__delete_lst)
        self.__clear_button = Button(self, text='Очистить список', command=self.__clear_lst)
        self.__choose_button = Button(self, text='Случайный элем.', command=self.__choose_lst)

    def __place_widgets(self):
        general_args = dict(sticky=NSEW, pady=10, padx=10)

        self.columnconfigure([0, 1], weight=1)
        self.rowconfigure([0, 1, 2, 3], weight=1)
        self.__main_list.grid(column=0, row=0, rowspan=4, **general_args)

        self.__append_button.grid(column=1, row=0, **general_args)
        self.__delete_button.grid(column=1, row=1, **general_args)
        self.__clear_button.grid(column=1, row=2, **general_args)
        self.__choose_button.grid(column=1, row=3, **general_args)

    def change_listsave(self, new_listname: str):
        self.__main_list.change_listsave(new_listname,
            save_current=not self.__curr_destroyed)
        
        if self.__curr_destroyed:
            self.activate()

    def __append_lst(self):
        new = askstring('Добавление элемента', 'Введите название нового элемента')
        if new == '': warning('Имя нового элемента не должно быть пустым')
        elif new is not None: self.__main_list.append(new)

    def __delete_lst(self):
        scfl = self.__main_list.remove()
        if not scfl: warning('Сначала выберите элемент из списка')

    def __clear_lst(self):
        yes = askyesno('Подтвердите действие', 'Вы точно хотите очистить список?')
        if yes: self.__main_list.clear()

    def __choose_lst(self):
        the_choosen_one = self.__main_list.choose()
        if the_choosen_one is None: error('Список пуст')
        else: info(the_choosen_one, title='Результат')

    def activate(self):
        self.__curr_destroyed = False
        self.__clear_button.config(state=NORMAL)
        self.__append_button.config(state=NORMAL)
        self.__delete_button.config(state=NORMAL)
        self.__choose_button.config(state=NORMAL)

    def deactivate(self):
        self.__curr_destroyed = True
        self.__clear_button.config(state=DISABLED)
        self.__append_button.config(state=DISABLED)
        self.__delete_button.config(state=DISABLED)
        self.__choose_button.config(state=DISABLED)


class SavesManager(Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, background=BACK_COL, **kwargs)
        self.__listname = 'guestlist'
        self.__listname_list = get_listname_list()

        self.__create_widgets()
        self.__place_widgets()

    def __create_widgets(self):
        self.__main_frame = MainFrame(self.__listname, self)

        self.__curr_save_lbl = Label(self, text=self.__listname)
        self.__comb = Combobox(self, values=self.__listname_list)

        self.__sel_button = Button(self,
            text='Открыть список',
            command=self.__change_listsave
        )

        self.__del_button = Button(self,
            text='Удалить список',
            command=self.__delete_lst
        )

    def __place_widgets(self):
        general_args = dict()

        self.columnconfigure([0, 1, 2], weight=1)
        self.rowconfigure([0, 1, 2], weight=1)

        self.__curr_save_lbl.grid(column=0, row=0, padx=5, sticky=EW, **general_args)
        self.__comb.grid(column=0, row=1, padx=3, **general_args)

        self.__sel_button.grid(column=1, row=0, rowspan=2, sticky=NS, **general_args)
        self.__del_button.grid(column=2, row=0, rowspan=2, sticky=NS, **general_args)

        self.__main_frame.grid(column=0, row=2, columnspan=3, pady=5, sticky=EW, **general_args)

    def __update_lstlst(self):
        self.__comb.config(values=self.__listname_list)

    def __change_listsave(self):
        input = self.__comb.get()

        if input:
            self.__main_frame.change_listsave(input)
            self.__listname = input
            self.__curr_save_lbl.config(text=input)

            if input not in self.__listname_list:
                self.__listname_list.insert(0, input)
                self.__update_lstlst()

        else: warning('Сначала вставите название списка')

    def __delete_lst(self):
        input = self.__comb.get()

        if not input: warning('Сначала вставьте имя списка в поле')
        elif input not in self.__listname_list: error('Список не найден')
        elif askyesno('Подтвердите действие', 'Вы точно хотите удалить список?'):
            self.__listname_list.remove(input)
            self.__update_lstlst()
            destroy_list(input)

            if self.__listname == input:
                self.__main_frame.deactivate()

            info('Список успешно удален')
