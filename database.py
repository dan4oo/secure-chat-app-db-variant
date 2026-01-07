import json
import urllib.request
from security import encrypt_message, hash_password, verify_password, encrypt_decrypt
from config import SUPABASE_URL, SUPABASE_PUBLISHABLE_DEFAULT_KEY as SUPABASE_KEY

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

import urllib.error

def _request(url, method="GET", data=None):
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as res:
            body = res.read()
            if body:  # Only parse if not empty
                return json.loads(body)
            return None
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print("HTTPError:", e.code, e.reason)
        print("Response body:", body)
        raise


def user_exists(username): #check if user exists
    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=id"
    res = _request(url)
    return bool(res)  # True if user found, False if empty

def create_user(username, password):
    hashed_password = hash_password(password)

    data = json.dumps({
        "username": username,
        "password": hashed_password
    }).encode()

    _request(f"{SUPABASE_URL}/rest/v1/users", "POST", data)

# Check if password matches
def check_password(username, password):
    """
    Returns True if the password matches the username in the database.
    Returns False if username not found or password does not match.
    """
    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=password"
    res = _request(url)
    
    if not res:
        return False  # User not found

    return verify_password(password, res[0]["password"])


def get_user_id(username): # get user id by username
    """Returns the id of a user, or None if not found"""
    url = f"{SUPABASE_URL}/rest/v1/users?username=eq.{username}&select=id"
    res = _request(url)
    if res:
        return res[0]["id"]
    return None
    
# Insert message
def insert_message(username, message, isLink, code):
    message = encrypt_message(message, code)
    user_id = get_user_id(username)
    data = json.dumps({"user_id": user_id, "message": message, "is_link": isLink}).encode()
    _request(f"{SUPABASE_URL}/rest/v1/messages", "POST", data)

# Get all messages
def get_all_messages():
    """
    Fetches all messages from the database and returns them as a list of dicts.
    Each dict contains: id, message, created_at, username
    """
    # Select message fields + username via foreign key embedding
    url = (
        f"{SUPABASE_URL}/rest/v1/messages?"
        f"select=id,message,created_at,is_link,users(username)&order=id"
    )
    res = _request(url)
    
    # Transform to flat list of objects
    messages = []
    if res:
        for m in res:
            messages.append({
                "id": m["id"],
                "message": m["message"],
                "is_link": m["is_link"],
                "created_at": m["created_at"],
                "username": m["users"]["username"]
            })
    return messages

# Check if database messages changed
def is_new_messages(local_messages_len):
    """
    Checks if the number of messages in the database differs from the local array.
    Returns:
        - True if new messages exist
        - False if no change
    """
    url = f"{SUPABASE_URL}/rest/v1/messages?select=id"
    res = _request(url)
    
    db_count = len(res) if res else 0
    local_count = local_messages_len

    return db_count != local_count

def delete_all_messages_for_user(username):
    user_id = get_user_id(username)

    _request(
        f"{SUPABASE_URL}/rest/v1/messages?user_id=eq.{user_id}",
        "DELETE"
    )


