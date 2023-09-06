import tkinter as tk
import sys
import threading
from threading import Event
import socket
import time

class Tk_Handler:
    def __init__(self, socket, need_to_login):
        self.type_player = 0
        self.socket = socket
        self.keep_waiting = True
        self.thread_event = Event()
        self.thread = None
        self.players = []
        self.requests = []
        self.__WINDOW_WIDTH = 713
        self.__WINDOW_HEIGHT = 563
        self.__BUTTON_FONT = ('Arial', 20)
        self.__LABEL_FONT = ('Arial', 80)
        self.__TITLE_FONT = ('Arial', 10)
        self.__SELECT_FONT = ('Arial', 65)
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

        self.__login = tk.Button(self.__beginning_page, text='Login', bg='lightgreen', font=self.__BUTTON_FONT, height=3, width=10, command=self.login)
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
        self.__username_taken.pack_forget()

        self.__already_signed_in = tk.Label(self.__register_page, text='already signed in', fg='red', bg='gray',width=20)
        self.__already_signed_in.pack_forget()

        # login page widgets -------------------------------------------------------------------
        self.__login_page = tk.Frame(self.root, bg='gray')

        self.__login_label = tk.Label(self.__login_page, text='Login', font=self.__LABEL_FONT, bg='blue')
        self.__login_label.pack(pady=20)

        # Input fields
        self.__invalid_key_login = tk.Label(self.__login_page, text='an invalid key was entered', fg='red', bg='gray',width=20)
        self.__invalid_key_login.pack_forget()

        # email
        self.__email_label_login = tk.Label(self.__login_page, text='Email:', font=self.__BUTTON_FONT, bg='gray')
        self.__email_label_login.pack(pady=5)

        self.__email_entry_login = tk.Entry(self.__login_page, font=self.__BUTTON_FONT, width=20)
        self.__email_entry_login.pack(pady=5)

        # password
        self.__password_label_login = tk.Label(self.__login_page, text='Password:', font=self.__BUTTON_FONT, bg='gray')
        self.__password_label_login.pack(pady=5)

        self.__password_entry_login = tk.Entry(self.__login_page, font=self.__BUTTON_FONT, width=20, show='*')
        self.__password_entry_login.pack(pady=5)

        # Buttons
        self.__button_frame = tk.Frame(self.__login_page, bg='gray')
        self.__button_frame.pack(pady=10)

        self.__back_button = tk.Button(self.__button_frame, text='Back', bg='lightblue', font=self.__BUTTON_FONT, command=self.main_page)
        self.__back_button.pack(side=tk.RIGHT, padx=5)

        self.__login_button = tk.Button(self.__button_frame, text='login', bg='lightblue', font=self.__BUTTON_FONT, command=self.login_button_pressed)
        self.__login_button.pack(padx=5)

        # Server Resposnes:
        self.__incorrect_login = tk.Label(self.__login_page, text='email or password incorrect', fg='red', bg='gray',width=20)
        self.__incorrect_login.pack_forget()

        # Start Page ---------------------------------------------------------------------------------:
        self.__start_page = tk.Frame(self.root, bg='gray')

        self.__hello_user = tk.Label(self.__start_page, text=f'hello', bg='gray', height=3, width=15, font=self.__TITLE_FONT)
        self.__hello_user.pack(pady=10)

        self.__start_button = tk.Button(self.__start_page, text='Start', bg='red', height=3, width=15, font=self.__BUTTON_FONT, command=self.select)
        self.__start_button.pack(pady=10)

        # enter loby code widgets------------------------------------------
        self.__select = tk.Frame(self.root, bg='gray')

        self.__select_code = tk.Label(self.__select, text='ask/join someone', bg='blue', height=1, width=15, font=self.__SELECT_FONT)
        self.__select_code.pack(pady=10)
        
        self.__create_loby = tk.Button(self.__select, text='join', bg='lightblue', font=self.__BUTTON_FONT, command=self.join)
        self.__create_loby.pack(pady=10)

        self.__join_loby = tk.Button(self.__select, text='ask', bg='lightblue', font=self.__BUTTON_FONT, command=self.ask)
        self.__join_loby.pack(pady=10)


        # ask widgets------------------------------------------
        self.__ask = tk.Frame(self.root, bg='gray')

        self.__ask_label = tk.Label(self.__ask, text='ask a player!', bg='blue', height=1, width=15, font=self.__SELECT_FONT)
        self.__ask_label.pack(pady=10)

        self.__refresh = tk.Button(self.__ask, text='refresh', bg='lightblue', font=self.__BUTTON_FONT, command=self.refresh)
        self.__refresh.pack(pady=10)

        self.__back_ask = tk.Button(self.__ask, text='back', bg='lightblue', font=self.__BUTTON_FONT, command=self.select)
        self.__back_ask.pack(pady=10)

        # # join widgets------------------------------------------
        self.__join = tk.Frame(self.root, bg='gray')

        self.__join_label = tk.Label(self.__join, text='join a player!', bg='blue', height=1, width=15, font=self.__SELECT_FONT)
        self.__join_label.pack(pady=10)

        self.__refresh_join = tk.Button(self.__join, text='refresh', bg='lightblue', font=self.__BUTTON_FONT, command=self.refresh_join)
        self.__refresh_join.pack(pady=10)

        self.__back_join = tk.Button(self.__join, text='back', bg='lightblue', font=self.__BUTTON_FONT, command=self.select)
        self.__back_join.pack(pady=10)

        # self.__refresh = tk.Button(self.__ask, text='refresh', bg='lightblue', font=self.__BUTTON_FONT, command=self.refresh)
        # self.__refresh.pack(pady=10)
        # -----------------------------------------------------------------

        # Show the original page by default
        if need_to_login:
            self.__show_page(self.__beginning_page)
        else:
            self.__show_page(self.__select)

    # Functions
    def __show_page(self, page):
        page.pack()

    def __hide_page(self, page):
        page.pack_forget()

    def register(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__select)
        self.__hide_page(self.__ask)
        self.__hide_page(self.__join)
        self.__show_page(self.__register_page)

    def login(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__select)
        self.__hide_page(self.__ask)
        self.__hide_page(self.__join)
        self.__show_page(self.__login_page)

    def start_page(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__select)
        self.__hide_page(self.__ask)
        self.__hide_page(self.__join)
        self.__show_page(self.__start_page)

    def main_page(self):
        self.__username_invalid.pack_forget()
        self.__email_invalid.pack_forget()
        self.__username_entry.delete(0, tk.END)
        self.__email_entry.delete(0, tk.END)
        self.__password_entry.delete(0, tk.END)
        self.__email_entry_login.delete(0, tk.END)
        self.__password_entry_login.delete(0, tk.END)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__ask)
        self.__hide_page(self.__join)
        self.__show_page(self.__beginning_page)

    def select(self):
        print('wowowowowowow')
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__ask)
        self.__hide_page(self.__join)
        self.__show_page(self.__select)

    def ask(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__select)
        self.__hide_page(self.__join)
        self.__show_page(self.__ask)
        self.refresh()

    def join(self):
        self.__hide_page(self.__beginning_page)
        self.__hide_page(self.__register_page)
        self.__hide_page(self.__login_page)
        self.__hide_page(self.__start_page)
        self.__hide_page(self.__select)
        self.__hide_page(self.__ask)
        self.__show_page(self.__join)
        self.refresh_join()
    
    def request(self, client):
        self.socket.send(f'RQ{client}'.encode())
        self.type_player = int(self.socket.recv(1024).decode()[-1])
        self.start_game()

    def reject(self, client):
        self.socket.send(f'RD{client}'.encode())  # Send a rejection message to the server
        self.refresh_join()  # Refresh the list of join requests

    def refresh_join(self):
        for request in self.requests:
            request.destroy()
        self.requests.clear()
        self.socket.send('RJ'.encode())
        clients = self.socket.recv(1024).decode().split(':')
        print(clients)
        if clients[0] == 'NC':
            return
        for client in clients:
            new_request_frame = tk.Frame(self.__join, bg='gray')  # Create a frame to contain the buttons
            new_request_frame.pack()
            self.requests.append(new_request_frame)

            accept_button = tk.Button(new_request_frame, text=f'Accept {client}?', bg='lightblue', font=self.__BUTTON_FONT, command=lambda client=client: self.request(client))
            accept_button.pack(side=tk.LEFT)
            self.requests.append(accept_button)

            no_button = tk.Button(new_request_frame, text=f'reject', bg='red', font=self.__BUTTON_FONT, command=lambda client=client: self.reject(client))
            no_button.pack(side=tk.LEFT)
            self.requests.append(no_button)

    def wait_for_info(self):
        data = self.socket.recv(1024).decode()
        if data[:2] == 'SG':
            self.type_player = int(data[-1])
            self.start_game()
        else:
            self.refresh()
            return

    def play(self, client):
        for player in self.players:
            player.destroy()
        self.socket.send(f'PY{client}'.encode())
        self.wait_for_info()

    def refresh(self):
        for player in self.players:
            player.destroy()
        self.players.clear()
        self.socket.send('RF'.encode())
        clients = self.socket.recv(1024).decode().split(':')
        if clients[0] == 'NC':
            return
        for client in clients:
            new_player = tk.Button(self.__ask, text=client, bg='lightblue', font=self.__BUTTON_FONT, command=lambda client=client: self.play(client))
            new_player.pack(pady=10)
            self.players.append(new_player)

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

    def login_button_pressed(self):
        self.__incorrect_login.pack_forget()
        self.__invalid_key_login.pack_forget()
        email = self.__email_entry_login.get()
        password = self.__password_entry_login.get()
        for character in self.invalid_characters:
            if character in email or character in password:
                self.__invalid_key_login.pack()
                return
        # if len(email) > 15:
        #     return
        # if len(password) > 15:
        #     return
        self.socket.send(f'LI{email}:{password}'.encode())
        data = self.socket.recv(1024).decode()
        if data[:2] == 'IL':
            self.__incorrect_login.pack()
            return
        else:
            self.username = data[2:]
            self.__hello_user.config(text=f'hello {self.username}')
            self.start_page()
        self.__username_entry.delete(0, tk.END)
        self.__email_entry.delete(0, tk.END)
        self.__password_entry.delete(0, tk.END)

    def start_game(self):
        self.root.destroy()
        self.game_started = True
    
    def exited(self):
        self.socket.send('goodbye'.encode())
        sys.exit()

    def start_program(self):
        self.root.protocol("WM_DELETE_WINDOW", self.exited)
        self.root.mainloop()