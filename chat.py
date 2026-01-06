import time
import threading
import os
import webbrowser
import getpass
from database import create_user, insert_message, get_all_messages, is_new_messages, user_exists, check_password
from config import POLL_INTERVAL
from security import encrypt_decrypt

userIsLoggedIn = False

def handleLogin():
    global username
    global code
    username = input("Enter your name: ").strip()
    password = getpass.getpass("Enter your password: ").strip()
    code = input("Enter room code: ").strip()
    if user_exists(username) is False:
        create_user(username, password)
        display_messages()
    elif check_password(username, password) is False:
        print("Incorrect password. Exiting.")
        exit(1)
    display_messages()

def terminal_link(text, url):
    return f"\033]8;;{url}\033\\{text}\033]8;;\033\\"


def display_messages():
    clear_terminal()
    current_user = None
    for m in messages:
        m["message"] = encrypt_decrypt(m["message"], code)
        if current_user != m["username"]:
            current_user = m["username"]
            print()
        if m["username"] == username:
            print(f"\033[90m{m['username']}: {m['message']}\033[0m")
        else:
            print(f"\033[93m\033[1m{m['username']}: {m['message']}\033[0m")
        if m["is_link"]:
            try:
                print("ne bachka linka oshte")
                # handle clickable link in terminal
            except Exception:
                pass

def clear_terminal():
    # Windows
    for times in range(20):
        print()
    if os.name == "nt":
        os.system("cls")
    # Mac/Linux
    else:
        os.system("clear")

def handleCommands(command):
    print(command[:6])
    print(command[6:])
    if command.lower() == "/exit":
        global running
        running = False
    elif command.lower() == "/logout":
        global userIsLoggedIn
        userIsLoggedIn = False
        handleLogin()
    elif command.lower()[:5] == "/link":
        insert_message(username, command[6:], True, code)
    else:
        print("Unknown command.")
    
messages = get_all_messages()
running = True


def listen():
    global messages
    while running:
        if is_new_messages(len(messages)):
            try:
                messages = get_all_messages()
                display_messages()
                print("> ", end="", flush=True)
            except Exception:
                pass
        time.sleep(POLL_INTERVAL)

threading.Thread(target=listen, daemon=True).start()

try:
    while running:
        if userIsLoggedIn is False:
            handleLogin()
            userIsLoggedIn = True
        text = input("> ").strip()
        if text:
            if text.lower()[0] == "/":
                handleCommands(text)
            elif text:
                insert_message(username, text, False, code)
        else:
            print("Please enter a message.")
except KeyboardInterrupt:
    running = False
