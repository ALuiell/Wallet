from tkinter import *
from tkinter import ttk


class MenuManager:

    def __init__(self, cat_manager, u_manager, acc_manager):

        self.main_menu_options_name = ["Управління категоріями витрат та доходів", "Управління рахунками",
                                       "Управління витратами та доходами", "Вихід"]

        self.category_manager = cat_manager
        self.user_manager = u_manager
        self.account_manager = acc_manager
        self.interface = Tk()
        self.menu_frame = Frame(self.interface)
        self.output_frame = Frame(self.interface)
        self.input_frame = Frame(self.interface)
        self.create_main_window()

    def create_main_window(self):

        def main_frame():
            self.interface.geometry("700x600")
            self.interface.minsize(700, 600)
            self.interface.maxsize(2000, 1900)
            self.interface.title("Wallet")
            self.interface.rowconfigure(0, weight=1)
            self.interface.rowconfigure(1, weight=1)
            self.interface.columnconfigure(0, weight=1)
            self.interface.columnconfigure(1, weight=1)

        def configure_frames():
            self.menu_frame.config(width=420, height=320, borderwidth=1, relief="solid")
            self.input_frame.config(width=420, height=280, borderwidth=1, relief="solid")
            self.output_frame.config(width=280, height=600, borderwidth=1, relief="solid")

        def menu_frame():
            self.menu_frame.grid(row=0, column=0, sticky="nw")

        def output_frame():
            self.output_frame.grid(row=0, column=1, rowspan=2, sticky="nsew")

        def input_frame():
            test_label = Label(self.input_frame, text="Це текст для перевірки меж input_frame", fg="red")
            test_label.pack()

        main_frame()
        configure_frames()

        menu_frame()
        output_frame()
        input_frame()

    def display_menu(self, dict_menu_options):
        self.clear_frame(self.menu_frame)

        row = 0
        for name, method in dict_menu_options.items():
            print(f"Створюємо кнопку: {name}")

            def handle_click(m=method):
                m()

            button = Button(self.menu_frame, text=name, command=handle_click,
                            bg="lightgrey", fg="black", font=("Helvetica", 14),
                            relief=RAISED, anchor="w", width=40)
            button.grid(row=row, column=0)
            row += 1

    def clear_frame(self, frame):
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()

    def generate_menu_dict(self, methods_name, list_menu_options):
        my_dict_generator = ((name, option) for name, option in zip(methods_name, list_menu_options))
        return dict(my_dict_generator)

    def create_menu(self, methods_name, list_menu_options):
        dict_menu_options = self.generate_menu_dict(methods_name, list_menu_options)
        self.clear_frame(self.menu_frame)
        self.display_menu(dict_menu_options)

    def main_menu(self):

        list_of_methods = (
            lambda: self.category_manager(self).category_manager_menu(),  # Викликаємо метод у лямбда-функції
            lambda: self.user_manager(self).user_manager_menu(),
            lambda: self.account_manager(self).account_manager_menu(),
            lambda: self.the_end()
        )

        dict_menu_options = self.generate_menu_dict(self.main_menu_options_name, list_of_methods)
        self.display_menu(dict_menu_options)

    def start(self):
        self.interface.mainloop()

    def the_end(self):
        self.interface.quit()
