#problem statement : Block chain and cryptocurrency Innovations
# Title :Enhanced Password Management with Tkinter GUI
from cryptography.fernet import Fernet
import sqlite3
import re
import tkinter as tk
from tkinter import messagebox

# Generate a random encryption key (keep this key secret)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Create a database or connect to an existing one
conn = sqlite3.connect("password_manager.db")
cursor = conn.cursor()

# Create a table to store passwords
cursor.execute('''CREATE TABLE IF NOT EXISTS passwords
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   website TEXT, 
                   username TEXT, 
                   password TEXT)''')
conn.commit()

def encrypt_password(password):
    # Encrypt the password using the same encryption key
    return cipher_suite.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    # Decrypt the password using the same encryption key
    return cipher_suite.decrypt(encrypted_password.encode()).decode()

def is_strong_password(password):
    # Define password policy rules
    min_length = 8
    has_lowercase = re.search(r'[a-z]', password)
    has_uppercase = re.search(r'[A-Z]', password)
    has_digit = re.search(r'\d', password)
    has_special_char = re.search(r'[!@#$%^&*()_+{}\[\]:;<>,.?~\\\-]', password)

    # Check if the password meets all the rules
    if (len(password) >= min_length and
        has_lowercase and
        has_uppercase and
        has_digit and
        has_special_char):
        return True
    else:
        return False

def add_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    
    if is_strong_password(password):
        # Encrypt the password before storing it
        encrypted_password = encrypt_password(password)

        cursor.execute("INSERT INTO passwords (website, username, password) VALUES (?, ?, ?)",
                       (website, username, encrypted_password))
        conn.commit()
        messagebox.showinfo("Success", "Password added successfully!")
    else:
        messagebox.showwarning("Weak Password", "Password is weak. It must have at least 8 characters, including at least one lowercase letter, one uppercase letter, one digit, and one special character.")

def view_passwords():
    cursor.execute("SELECT * FROM passwords")
    passwords = cursor.fetchall()
    if passwords:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        for password in passwords:
            decrypted_password = decrypt_password(password[3])
            result_text.insert(tk.END, f"Website: {password[1]}, Username: {password[2]}, Password: {decrypted_password}\n")
        result_text.config(state=tk.DISABLED)
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, "No passwords stored yet.")
        result_text.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("Password Manager")

# Entry Widgets
website_entry = tk.Entry(root, width=30)
username_entry = tk.Entry(root, width=30)
password_entry = tk.Entry(root, width=30, show='*')

# Labels
website_label = tk.Label(root, text="Website:")
username_label = tk.Label(root, text="Username:")
password_label = tk.Label(root, text="Password:")

# Buttons
add_button = tk.Button(root, text="Add Password", command=add_password)
view_button = tk.Button(root, text="View Passwords", command=view_passwords)

# Text widget for displaying passwords
result_text = tk.Text(root, height=10, width=50, state=tk.DISABLED)

# Layout
website_label.grid(row=0, column=0, padx=10, pady=5)
website_entry.grid(row=0, column=1, padx=10, pady=5)
username_label.grid(row=1, column=0, padx=10, pady=5)
username_entry.grid(row=1, column=1, padx=10, pady=5)
password_label.grid(row=2, column=0, padx=10, pady=5)
password_entry.grid(row=2, column=1, padx=10, pady=5)
add_button.grid(row=3, column=0, columnspan=2, pady=10)
view_button.grid(row=4, column=0, columnspan=2, pady=10)
result_text.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
