import tkinter as tk
from tkinter import ttk
from main import setup_database, fetch_passwords, generate_password, save_password
import random

# Initialize the main window
root = tk.Tk()

# Global UI variables
entry = None
password_var = None
status_label = None

def copy_to_clipboard(text):
    """Copies the given text to the system clipboard and updates the status message."""
    if not text:
        return
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Now the text is in the clipboard
    # Update the status message
    status_label.config(text="The password was successfully copied", fg="green")

def on_generate():
    """Handles the password generation process."""
    input_text = entry.get().strip()
    if not input_text:
        status_label.config(text="Please enter some text!", fg="red")
        return

    password = generate_password(input_text, length=12)
    password_var.set(password)
    save_password(input_text, password)
    status_label.config(text="Password generated and stored!", fg="green")

def on_tree_click(event, tree):
    """
    When a row in the table is clicked, copy the corresponding password to the clipboard.
    """
    region = tree.identify("region", event.x, event.y)
    if region == "cell":
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            password = item["values"][1]  # second column holds the password
            copy_to_clipboard(password)

def show_saved_passwords(order_by="date_time", ascending=False, search_query=""):
    # Clear the main window
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Saved Passwords", font=("Calibri", 18, "bold")).pack(pady=10)

    # Search bar frame (created only once)
    search_frame = tk.Frame(root)
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Search:", font=("Calibri", 12)).pack(side="left", padx=5)
    
    # Use a global variable to persist the search value between updates
    global search_var
    search_var = tk.StringVar(value=search_query)
    search_entry = tk.Entry(search_frame, font=("Calibri", 12), width=30, textvariable=search_var)
    search_entry.pack(side="left")

    # Create a frame for the table so we can update it separately
    table_frame = tk.Frame(root, borderwidth=2, relief="solid")
    table_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def update_table(*args):
        # Clear only the table_frame contents (keep the search bar intact)
        for widget in table_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(table_frame, columns=("Input Text", "Password", "Date/Time"), show="headings", height=10)
        tree.pack(expand=True, fill="both")

        ascending_sort = not ascending

        def sort_by_input():
            show_saved_passwords(order_by="input_text", ascending=ascending_sort, search_query=search_var.get())
        def sort_by_date():
            show_saved_passwords(order_by="date_time", ascending=ascending_sort, search_query=search_var.get())

        tree.heading("Input Text", text="Input Text ▲▼", anchor="center", command=sort_by_input)
        tree.heading("Password", text="Password", anchor="center")
        tree.heading("Date/Time", text="Date/Time ▲▼", anchor="center", command=sort_by_date)
        tree.column("Input Text", width=150, anchor="center")
        tree.column("Password", width=150, anchor="center")
        tree.column("Date/Time", width=200, anchor="center")

        rows = fetch_passwords(order_by, ascending, search_var.get())
        for row in rows:
            input_text, password, date_time = row
            tree.insert("", "end", values=(input_text, password, date_time))

        tree.bind("<ButtonRelease-1>", lambda e: on_tree_click(e, tree))

    # Bind the trace so that changes update only the table
    search_var.trace_add("write", update_table)
    # Populate the table initially
    update_table()

    global status_label
    status_label = tk.Label(root, text="", font=("Calibri", 12))
    status_label.pack()
    back_button = tk.Button(root, text="Back", font=("Calibri", 14), command=show_main_page)
    back_button.pack(pady=10)


def show_main_page():
    """Restores the main password generator page."""
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Enter text:", font=("Calibri", 14)).pack(pady=5)
    global entry
    entry = tk.Entry(root, width=40, font=("Calibri", 14))
    entry.pack(pady=5)

    generate_button = tk.Button(root, text="Generate Password", font=("Calibri", 14), command=on_generate)
    generate_button.pack(pady=10)

    global password_var
    password_var = tk.StringVar()
    password_label = tk.Label(root, textvariable=password_var, font=("Calibri", 16, "bold"), fg="green")
    password_label.pack(pady=5)

    copy_button = tk.Button(root, text="Copy to Clipboard", font=("Calibri", 14),
                            command=lambda: copy_to_clipboard(password_var.get()))
    copy_button.pack(pady=5)

    view_button = tk.Button(root, text="View Saved Passwords", font=("Calibri", 14), command=show_saved_passwords)
    view_button.pack(pady=10)

    global status_label
    status_label = tk.Label(root, text="", font=("Calibri", 12), fg="black")
    status_label.pack(pady=5)

def run_app():
    """Initializes the database and starts the Tkinter main loop."""
    setup_database()
    root.title("Password Generator with Database")
    root.geometry("550x450")
    show_main_page()
    root.mainloop()

if __name__ == "__main__":
    run_app()
