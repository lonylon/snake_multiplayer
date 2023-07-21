import tkinter as tk

class Tk_Handler:
    def __init__(self):
        self.__WINDOW_WIDTH = 713
        self.__WINDOW_HEIGHT = 563
        self.__BUTTON_FONT = ('Arial', 20)
        self.__LABEL_FONT = ('Arial', 80)
        self.__TITLE_FONT = ('Arial', 30)
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry(f'{self.__WINDOW_WIDTH}x{self.__WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.root.configure(bg='gray')
        self.game_started = False

        # Original page widgets --------------------------------------------------------------
        self.__start_page = tk.Frame(self.root, bg='gray')

        self.__start_button = tk.Button(self.__start_page, text='Start', bg='red', font=self.__TITLE_FONT, command=self.start_game)
        self.__start_button.pack(pady=10)

        self.__snake_label = tk.Label(self.__start_page, text='Snake', bg='green', font=self.__LABEL_FONT)
        self.__snake_label.pack(pady=10)

        self.__login = tk.Button(self.__start_page, text='Login', bg='lightgreen', font=self.__BUTTON_FONT, height=3, width=10)
        self.__login.pack(pady=10)

        self.__register = tk.Button(self.__start_page, text='Register', bg='lightgreen', font=self.__BUTTON_FONT, height=3, width=10, command=self.register)
        self.__register.pack(pady=10)

        # Register page widgets -------------------------------------------------------------------
        self.__register_page = tk.Frame(self.root, bg='gray')

        self.__register_label = tk.Label(self.__register_page, text='Register', font=self.__LABEL_FONT, bg='blue')
        self.__register_label.pack(pady=20)

        # Input fields
        # username:
        self.__username_label = tk.Label(self.__register_page, text='Username:', font=self.__BUTTON_FONT, bg='gray')
        self.__username_label.pack(pady=5)

        self.__username_entry = tk.Entry(self.__register_page, font=self.__BUTTON_FONT, width=20)
        self.__username_entry.pack(pady=5)
        # email
        self.__email_label = tk.Label(self.__register_page, text='Email:', font=self.__BUTTON_FONT, bg='gray')
        self.__email_label.pack(pady=5)

        self.__email_entry = tk.Entry(self.__register_page, font=self.__BUTTON_FONT, width=20)
        self.__email_entry.pack(pady=5)
        # password
        self.__password_label = tk.Label(self.__register_page, text='Password:', font=self.__BUTTON_FONT, bg='gray')
        self.__password_label.pack(pady=5)

        self.__password_entry = tk.Entry(self.__register_page, font=self.__BUTTON_FONT, width=20, show='*')
        self.__password_entry.pack(pady=5)

        # Buttons
        self.__button_frame = tk.Frame(self.__register_page, bg='gray')
        self.__button_frame.pack(pady=10)

        self.__back_button = tk.Button(self.__button_frame, text='Back', bg='lightblue', font=self.__BUTTON_FONT, command=self.main_page)
        self.__back_button.pack(side=tk.RIGHT, padx=5)

        self.__login_button = tk.Button(self.__button_frame, text='Login', bg='lightblue', font=self.__BUTTON_FONT, command=self.login_button_pressed)
        self.__login_button.pack(padx=5)

        # Show the original page by default
        self.__show_page(self.__start_page)

        self.root.mainloop()

    # Functions
    def __show_page(self, page):
        if not self.game_started:
           page.pack()

    def __hide_page(self, page):
        if not self.game_started:
            page.pack_forget()

    def register(self):
        self.__hide_page(self.__start_page)
        self.__show_page(self.__register_page)

    def main_page(self):
        self.__hide_page(self.__register_page)
        self.__show_page(self.__start_page)

    def login_button_pressed(self):
        username = self.__username_entry.get()
        email = self.__email_entry.get()
        password = self.__password_entry.get()
        print("Username:", username)
        print('email:', email)
        print("Password:", password)
        self.__username_entry.delete(0, tk.END)
        self.__email_entry.delete(0, tk.END)
        self.__password_entry.delete(0, tk.END)
    
    def start_game(self):
        self.root.destroy()
        self.game_started = True
