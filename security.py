import hashlib
import secrets
import base64

def hash_password(password: str) -> str:
    """
    Returns a salted SHA-256 hash in the format:
    salt$hash
    """
    salt = secrets.token_hex(16)  # random 32-char salt
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"{salt}${hashed}"

def verify_password(password: str, stored_value: str) -> bool:
    """
    Verifies a password against the stored salt$hash
    """
    salt, stored_hash = stored_value.split("$")
    hashed = hashlib.sha256((salt + password).encode()).hexdigest()
    return hashed == stored_hash


def derive_key(code, length=256):
    # Turn room code into a byte key
    digest = hashlib.sha256(code.encode()).digest()
    # repeat to match message length
    return digest

def encrypt_decrypt(message, code):
    key = derive_key(code)
    result = []
    for i, char in enumerate(message):
        result.append(chr(ord(char) ^ key[i % len(key)]))
    return "".join(result)

def encrypt_message(message: str, code: str) -> str:
    encrypted = encrypt_decrypt(message, code)   # your XOR function
    encrypted_bytes = encrypted.encode("utf-8", errors="ignore")
    return base64.b64encode(encrypted_bytes).decode("ascii")

def decrypt_message(stored_value: str, code: str) -> str:
    try:
        encrypted_bytes = base64.b64decode(stored_value.encode("ascii"))
        encrypted = encrypted_bytes.decode("utf-8", errors="ignore")
        return encrypt_decrypt(encrypted, code)
    except Exception:
        return "[Decryption Error] possibly wrong room code"