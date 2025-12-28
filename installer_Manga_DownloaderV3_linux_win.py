import os
import platform
import urllib.request
import zipfile
import shutil
import subprocess

# URL du projet GitHub (ZIP)
URL = "https://github.com/romhackman/Manga/archive/refs/heads/main.zip"

# Dossiers utilisateur
HOME = os.path.expanduser("~")
DOWNLOADS = os.path.join(HOME, "Téléchargements")
DOCUMENTS = os.path.join(HOME, "Documents")

ZIP_PATH = os.path.join(DOWNLOADS, "Manga.zip")
EXTRACT_PATH = os.path.join(DOCUMENTS, "Manga-main")
FINAL_PATH = os.path.join(DOCUMENTS, "Manga")

print("📥 Téléchargement du programme Manga...")

# Télécharger le ZIP
urllib.request.urlretrieve(URL, ZIP_PATH)

print("📦 Extraction du ZIP...")

# Extraire le ZIP
with zipfile.ZipFile(ZIP_PATH, 'r') as zip_ref:
    zip_ref.extractall(DOCUMENTS)

# Supprimer le ZIP après extraction
if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)
    print("🗑️ ZIP supprimé après extraction")

# Supprimer ancien dossier Manga si existant
if os.path.exists(FINAL_PATH):
    shutil.rmtree(FINAL_PATH)

# Renommer le dossier
os.rename(EXTRACT_PATH, FINAL_PATH)

print("✅ Installation terminée")

# Choix du système
print("\nQuel est ton système ?")
print("1 - Windows")
print("2 - Linux")

choice = input("Choix (1 ou 2) : ").strip()

os.chdir(FINAL_PATH)

if choice == "1":
    print("🪟 Lancement de setup_win.py...")
    subprocess.run(["python", "setup_win.py"])

elif choice == "2":
    print("🐧 Lancement de setup_linux.py...")
    subprocess.run(["python3", "setup_linux.py"])

else:
    print("❌ Choix invalide")
