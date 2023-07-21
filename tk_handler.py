import tkinter as tk
import sys

class Tk_Handler:
    def __init__(self, socket):
        self.socket = socket
        self.__WINDOW_WIDTH = 713
        self.__WINDOW_HEIGHT = 563
        self.__BUTTON_FONT = ('Arial', 20)
        self.__LABEL_FONT = ('Arial', 80)
        self.__TITLE_FONT = ('Arial', 10)
        self.invalid_characters = [';', ':', ',', ' ', '/','\\']
        self.username = ''
        # Create the main window
        self.root = tk.Tk()
        self.root.geometry(f'{self.__WINDOW_WIDTH}x{self.__WINDOW_HEIGHT}')
        self.root.resizable(False, False)
        self.root.configure(bg='gray')
        self.game_started = False

        # Original page widgets --------------------------------------------------------------
        self.__beginning_page = tk.Frame(self.root, bg='gray')

        self.__snake_label = tk.Label(self.__beginning_page, text='Snake', bg='green', font=self.__LABEL_FONT)
        self.__snake_label.pack(pady=10)

        self.__login = tk.Button(self.__beginning_page, text='Login', bg='lightgreen', font=self.__BUTTON_FONT, height=3, width=10)
        self.__login.pack(pady=10)

        self.__register = tk.Button(self.__beginning_page, text='Register', bg='lightgreen', font=self.__BUTTON_FONT, height=3, width=10, command=self.register)
        self.__register.pack(pady=10)

        # Register page widgets -------------------------------------------------------------------
        self.__register_page = tk.Frame(self.root, bg='gray')

        self.__register_label = tk.Label(self.__register_page, text='Register', font=self.__LABEL_FONT, bg='blue')
        self.__register_label.pack(pady=20)

        # Input fields
        self.__invalid_key = tk.Label(self.__register_page, text='an invalid key was entered', fg='red', bg='gray',width=20)
        self.__invalid_key.pack_forget()

        # username:
        self.__username_label = tk.Label(self.__register_page, text='Username:', font=self.__BUTTON_FONT, bg='gray')
        self.__username_label.pack(pady=5)

        self.__username_entry = tk.Entry(self.__register_page, font=self.__BUTTON_FONT, width=20)
        self.__username_entry.pack(padx=5)

        self.__username_invalid = tk.Label(self.__register_page, text='invalid unsername', fg='red', bg='gray',width=20)
        self.__username_invalid.pack_forget()
        # email
        self.__email_label = tk.Label(self.__register_page, text='Email:', font=self.__BUTTON_FONT, bg='gray')
        self.__email_label.pack(pady=5)

        self.__email_entry = tk.Entry(self.__register_page, font=self.__BUTTON_FONT, width=20)
        self.__email_entry.pack(pady=5)

        self.__email_invalid = tk.Label(self.__register_page, text='invalid email', fg='red', bg='gray',width=20)
        self.__email_invalid.pack_forget()
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

        self.__login_button = tk.Button(self.__button_frame, text='Register', bg='lightblue', font=self.__BUTTON_FONT, command=self.register_button_pressed)
        self.__login_button.pack(padx=5)

        # Server Resposnes:
        self.__username_taken = tk.Label(self.__register_page, text='username taken', fg='red', bg='gray',width=20)
        self.__email_invalid.pack_forget()

        self.__already_signed_in = tk.Label(self.__register_page, text='already signed in', fg='red', bg='gray',width=20)
        self.__email_invalid.pack_forget()

        # Start Page:
        self.__start_page = tk.Frame(self.root, bg='gray')

        self.__hello_user = tk.Label(self.__start_page, text=f'hello', bg='gray', height=3, width=15, font=self.__TITLE_FONT)
        self.__hello_user.pack(pady=10)

        self.__start_button = tk.Button(self.__start_page, text='Start', bg='red', height=3, width=15, font=self.__BUTTON_FONT, command=self.start_game)
        self.__start_button.pack(pady=10)

        # Show the original page by default
        self.__show_page(self.__beginning_page)

    # Functions
    def __show_page(self, page):
        page.pack()

    def __hide_page(self, page):
        page.pack_forget()

    def register(self):
        self.__hide_page(self.__beginning_page)
        self.__show_page(self.__register_page)

    def start_page(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__register_page)
        self.__show_page(self.__start_page)

    def main_page(self):
        self.__username_invalid.pack_forget()
        self.__email_invalid.pack_forget()
        self.__username_entry.delete(0, tk.END)
        self.__email_entry.delete(0, tk.END)
        self.__password_entry.delete(0, tk.END)
        self.__hide_page(self.__register_page)
        self.__show_page(self.__beginning_page)

    def register_button_pressed(self):
        self.__invalid_key.pack_forget()
        self.__email_invalid.pack_forget()
        self.__username_invalid.pack_forget()
        self.__already_signed_in.pack_forget()
        self.__username_taken.pack_forget()
        username = self.__username_entry.get()
        email = self.__email_entry.get()
        password = self.__password_entry.get()
        for character in self.invalid_characters:
            if character in username or character in email or character in password:
                self.__invalid_key.pack()
                return
        if len(username) > 15:
            self.__username_invalid.pack()
            return
        if len(email) > 15:
            self.__email_invalid.pack()
            return
        if len(password) > 15:
            return
        self.socket.send(f'RE{username}:{email}:{password}'.encode())
        data = self.socket.recv(1024).decode()
        if data == 'AS':
            self.__already_signed_in.pack()
            return
        elif data == 'UT':
            self.__username_taken.pack()
            return
        else:
            self.username = username
            self.__hello_user.config(text=f'hello {username}')
            self.start_page()
        self.__username_entry.delete(0, tk.END)
        self.__email_entry.delete(0, tk.END)
        self.__password_entry.delete(0, tk.END)

    def start_game(self):
        self.root.destroy()
        self.game_started = True
    

    def start_program(self):
        self.root.protocol("WM_DELETE_WINDOW", sys.exit)
        self.root.mainloop()