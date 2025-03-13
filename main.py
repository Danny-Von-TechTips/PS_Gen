import hashlib
import random
import string
import sqlite3
from datetime import datetime

# Database filename
DB_FILE = "passwords.db"

def setup_database():
    """Creates the database table if it doesn't exist."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS passwords (
            input_text TEXT PRIMARY KEY,
            password TEXT,
            date_time TEXT
        )
    ''')
    conn.commit()
    conn.close()

def fetch_passwords(order_by="date_time", ascending=False, search_query=""):
    """
    Fetches stored passwords from the database with sorting and filtering.
    :param order_by: which column to sort by
    :param ascending: boolean for ascending vs descending order
    :param search_query: a string to filter results by `input_text`
    :return: list of rows (input_text, password, date_time)
    """
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    order_clause = f"{order_by} {'ASC' if ascending else 'DESC'}"

    if search_query:
        cursor.execute(
            f"SELECT * FROM passwords WHERE input_text LIKE ? ORDER BY {order_clause}",
            ('%' + search_query + '%',)
        )
    else:
        cursor.execute(f"SELECT * FROM passwords ORDER BY {order_clause}")

    rows = cursor.fetchall()
    conn.close()
    return rows

def generate_password(input_text, length=12):
    """
    Generates a strong password that includes:
      - Lowercase letters
      - Uppercase letters
      - Digits
      - Special characters
    Uses the user input_text to seed a hash, then randomizes further.
    :param input_text: the text that seeds our password generation
    :param length: desired minimum length of the generated password
    :return: randomized, strong password as a string
    """
    # Create a SHA-256 hash based on the input_text
    hash_object = hashlib.sha256(input_text.encode())
    hash_hex = hash_object.hexdigest()

    # Define character sets
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    digits = string.digits
    specials = "!@#$%^&*()_+<>?~"

    # Ensure at least one character from each category
    random_part = [
        random.choice(lower),
        random.choice(upper),
        random.choice(digits),
        random.choice(specials)
    ]

    remaining_length = max(length - len(random_part), 0)
    char_pool = lower + upper + digits + specials

    # Use parts of the hash to deterministically add more characters
    for i in range(0, 2 * remaining_length, 2):
        if i + 1 < len(hash_hex):
            chunk = hash_hex[i:i+2]
            value = int(chunk, 16)
            random_part.append(char_pool[value % len(char_pool)])
        else:
            random_part.append(random.choice(char_pool))

    # Shuffle the list to mix the characters
    random.shuffle(random_part)
    return "".join(random_part)

def save_password(input_text, password):
    """
    Saves the generated password in the database (unique by input_text).
    :param input_text: the seed text
    :param password: the generated password
    """
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO passwords (input_text, password, date_time)
        VALUES (?, ?, ?)
    ''', (input_text, password, date_time))
    conn.commit()
    conn.close()
