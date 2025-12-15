import os
import zipfile
import urllib.request
import subprocess
import shutil
import sys
import ctypes

# CONFIG
GITHUB_ZIP_URL = "https://github.com/romhackman/Manga/archive/refs/heads/main.zip"
PROJECT_NAME = "Manga"

DOWNLOADS_DIR = os.path.join(os.path.expanduser("~"), "Downloads")
ZIP_PATH = os.path.join(DOWNLOADS_DIR, "Manga.zip")
TARGET_DIR = os.path.join(DOWNLOADS_DIR, PROJECT_NAME)

APPDATA_DIR = os.getenv("APPDATA")

def download_repo():
    print("⬇️ Téléchargement du dépôt Manga (GitHub)...")

    req = urllib.request.Request(
        GITHUB_ZIP_URL,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req) as response:
        with open(ZIP_PATH, "wb") as f:
            f.write(response.read())

def extract_repo():
    print("📂 Extraction...")
    with zipfile.ZipFile(ZIP_PATH, "r") as zip_ref:
        zip_ref.extractall(DOWNLOADS_DIR)

    os.remove(ZIP_PATH)

    source_path = os.path.join(DOWNLOADS_DIR, "Manga-main")

    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)

    shutil.move(source_path, TARGET_DIR)

def run_setup():
    print("⚙️ Lancement de setup.py...")
    subprocess.check_call(
        [sys.executable, "setup.py"],
        cwd=TARGET_DIR
    )

def ask_user_to_move():
    message = (
        "Installation terminée.\n\n"
        "Veuillez maintenant déplacer :\n"
        "- le fichier Manga.exe\n"
        "- le dossier Manga\n\n"
        f"VERS :\n{APPDATA_DIR}\n\n"
        "Les dossiers vont s'ouvrir automatiquement."
    )

    ctypes.windll.user32.MessageBoxW(
        0, message, "Manga - Installation", 0
    )

    os.startfile(DOWNLOADS_DIR)
    os.startfile(APPDATA_DIR)

def main():
    download_repo()
    extract_repo()
    run_setup()
    ask_user_to_move()

if __name__ == "__main__":
    main()
