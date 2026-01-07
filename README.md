Terminal Chat App (Encrypted, DB based)

A simple terminal-based chat application written in Python.
Supports multiple users in a single chat room, with encrypted messages using a room code.

Messages are stored in Supabase, and passwords are hashed. Users can encrypt chat messages with a shared room code.

Features

Single shared chat room for multiple users

User registration and login with hashed passwords

Messages are encrypted using a room code

Terminal-based interface with colored output

Commands:

/help — show all available commands

/exit — exit the app

/logout — log out current user --fixed

/link <url> — send a clickable link --TODO

/deletemine — delete all your messages from the database

Installation

Works without extra installs for basic functionality.
For proper message encryption, cryptography is required.

1. Clone the repository
git clone https://github.com/yourusername/terminal-chat-app.git
cd terminal-chat-app

2. (Optional) Virtual environment (recommended)
python3 -m venv .venv
source .venv/bin/activate

Setup

Create a Supabase project

Configure the following tables:

users

Column	Type	Notes
id	UUID	Primary key
username	Text	Unique
password	Text	Hashed password
created_at	Timestamp	Default now()

messages

Column	Type	Notes
id	UUID	Primary key
user_id	UUID	Foreign key to users
message	Text	Encrypted or plaintext
is_link	Boolean	True if message is a link
created_at	Timestamp	Default now()

Create the config.py with your Supabase URL and anon key.

Usage
python3 chat.py


Register or login with username and password (If the username doesn't exists in the database it automaticaly creates the user)

Enter messages in the terminal

Use /link <url> to send clickable links --TODO

Encryption

When prompted for a room code, messages are encrypted/decrypted automatically

Without the correct code, messages will appear as gibberish

Supports XOR-based encryption (no install) (with bas64)

Security Notes

Passwords are stored hashed, never in plaintext

XOR encryption is not secure, only obfuscates messages

Never share the Supabase service key — keep it on a secure server if you move to production

Example Commands
/help          # shows all the available commands
/exit          # Close the application
/logout        # Log out current user
/link <url>    # Send a clickable link
/deletemine    # deletes all your messages from the database
-more to come

Dependencies

Python 3.10+

Supabase (hosted PostgreSQL backend)

License

MIT License — free to use, modify, and distribute.
