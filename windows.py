from frames import *


class MainWindow(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Lucas\' Listland')
        self.resizable(False, False)
        self.config(background=BACK_COL)

        self.__init_widgets()

    def __init_widgets(self):
        self.__main_frame = SavesManager(self)
        self.__main_frame.pack(expand=True, fill=BOTH, padx=10, pady=10, ipadx=5, ipady=5)

    def open(self):
        self.mainloop()
