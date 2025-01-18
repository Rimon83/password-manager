from cryptography.fernet import Fernet
import sys
import os


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS2
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# generate key
key = Fernet.generate_key()
# read main file
with open(resource_path("main.py"), "rb") as file:
    original_code = file.read()

# Encrypt the Python script
cipher = Fernet(key)
encrypted_code = cipher.encrypt(original_code)

# Decrypt the script
decrypted_code = cipher.decrypt(encrypted_code)

# Execute the decrypted Python code
exec(decrypted_code.decode("utf-8"))
