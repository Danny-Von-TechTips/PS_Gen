import hashlib
import random
import tkinter as tk
from tkinter import messagebox

def generate_password():
    input_text = entry.get()
    if not input_text:
        status_label.config(text="Please enter some text!", fg="red")
        return

    # Generate SHA-256 hash
    hash_object = hashlib.sha256(input_text.encode())
    hash_hex = hash_object.hexdigest()

    # Take first 10 characters
    first_10_chars = hash_hex[:14]

    # Add uppercase letter and special character
    uppercase_letter = chr(random.randint(65, 90))  # A-Z
    special_characters = "!@#$%^&*()_+<>?"
    special_character = random.choice(special_characters)

    # Combine and shuffle
    password = list(first_10_chars + uppercase_letter + special_character)
    random.shuffle(password)
    generated_password.set("".join(password))
    status_label.config(text="Password generated successfully!", fg="green")

def copy_to_clipboard():
    password = generated_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        root.update()
        status_label.config(text="Password copied to clipboard!", fg="blue")
    else:
        status_label.config(text="No password to copy!", fg="red")

# Create GUI window
root = tk.Tk()
root.title("Password Generator")
root.geometry("400x300")

# Input field
tk.Label(root, text="Enter text:").pack(pady=5)
entry = tk.Entry(root, width=30)
entry.pack(pady=5)

# Generate button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.pack(pady=10)

# Display generated password
generated_password = tk.StringVar()
password_label = tk.Label(root, textvariable=generated_password, font=("Arial", 12, "bold"), fg="green")
password_label.pack(pady=5)

# Copy button
copy_button = tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=10)

# Status message label
status_label = tk.Label(root, text="", fg="black")
status_label.pack(pady=5)

# Run GUI loop
root.mainloop()


