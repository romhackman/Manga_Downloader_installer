import os
import urllib.request
import zipfile
import shutil
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# URL du projet GitHub
URL = "https://github.com/romhackman/Manga/archive/refs/heads/main.zip"

def download_and_extract():
    # Demander le dossier d'extraction
    extract_folder = filedialog.askdirectory(title="Choisissez le dossier où extraire Manga")
    if not extract_folder:
        messagebox.showwarning("Avertissement", "Aucun dossier sélectionné. Abandon.")
        return

    zip_path = os.path.join(extract_folder, "Manga.zip")
    extract_path = os.path.join(extract_folder, "Manga-main")
    final_path = os.path.join(extract_folder, "Manga")

    try:
        # Télécharger le ZIP
        status_label.config(text="📥 Téléchargement en cours...")
        root.update()
        urllib.request.urlretrieve(URL, zip_path)

        # Extraire le ZIP
        status_label.config(text="📦 Extraction en cours...")
        root.update()
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)

        # Supprimer le ZIP après extraction
        if os.path.exists(zip_path):
            os.remove(zip_path)

        # Supprimer ancien dossier Manga si existant
        if os.path.exists(final_path):
            shutil.rmtree(final_path)

        # Renommer le dossier
        os.rename(extract_path, final_path)

        status_label.config(text="✅ Extraction terminée")

        # Demander le système
        system_choice = messagebox.askquestion("Système", "Utilisez-vous Windows ? (Sinon Linux)")

        # Lancer le setup approprié
        os.chdir(final_path)
        if system_choice == "yes":
            status_label.config(text="🪟 Lancement de setup_win.py...")
            root.update()
            subprocess.run(["python", "setup_win.py"])
            messagebox.showinfo("Terminé", "Installation terminée ! Pour lancer l'application, utilisez : Launcher.vbs")
        else:
            status_label.config(text="🐧 Lancement de setup_linux.py...")
            root.update()
            subprocess.run(["python3", "setup_linux.py"])
            messagebox.showinfo("Terminé", "Installation terminée ! Pour lancer l'application, utilisez : launch.sh")

    except Exception as e:
        messagebox.showerror("Erreur", str(e))

# Interface Tkinter
root = tk.Tk()
root.title("Installateur Manga")
root.geometry("450x200")

tk.Label(root, text="Installer Manga depuis GitHub", font=("Arial", 14)).pack(pady=10)

status_label = tk.Label(root, text="Cliquez sur 'Télécharger et Installer'", fg="blue")
status_label.pack(pady=10)

tk.Button(root, text="Télécharger et Installer", command=download_and_extract, width=30, height=2).pack(pady=20)

root.mainloop()
