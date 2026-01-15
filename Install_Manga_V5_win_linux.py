import os
import sys
import urllib.request
import zipfile
import shutil
import subprocess
import platform
import traceback

# ===================== CONFIG =====================
# URL du projet GitHub
URL = "https://github.com/romhackman/Manga/archive/refs/heads/main.zip"

# Codes couleurs ANSI pour Windows et Linux
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'

# Pour Windows CMD qui ne supporte pas ANSI par défaut
if platform.system() == "Windows":
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# ===================== FONCTIONS =====================
def print_success(msg):
    print(f"{Colors.GREEN}{msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}{msg}{Colors.END}")

def print_warn(msg):
    print(f"{Colors.YELLOW}{msg}{Colors.END}")

def run(cmd, fail_msg=""):
    """Exécute une commande shell et affiche une erreur sans fermer le CMD"""
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError:
        print_error(f"❌ Échec de l'exécution : {cmd}")
        if fail_msg:
            print_error(fail_msg)
        print_error("⚠ Le script continue, vérifiez les messages ci-dessus.")
        traceback.print_exc()

def check_python_version():
    if sys.version_info < (3, 10):
        print_warn(f"⚠ Votre version de Python est {sys.version.split()[0]}. Il est recommandé d'utiliser Python >= 3.10.")

def download_and_extract(dest_folder):
    zip_path = os.path.join(dest_folder, "Manga.zip")
    extract_path = os.path.join(dest_folder, "Manga-main")
    final_path = os.path.join(dest_folder, "Manga")

    print("📥 Téléchargement du projet GitHub...")
    try:
        urllib.request.urlretrieve(URL, zip_path)
    except Exception as e:
        print_error(f"❌ Échec du téléchargement : {e}")
        return None

    print("📦 Extraction du projet...")
    try:
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(dest_folder)
        os.remove(zip_path)
        if os.path.exists(final_path):
            shutil.rmtree(final_path)
        os.rename(extract_path, final_path)
        print_success(f"✅ Projet extrait dans : {final_path}")
        return final_path
    except Exception as e:
        print_error(f"❌ Erreur lors de l'extraction : {e}")
        return None

def create_venv(project_path):
    venv_path = os.path.join(project_path, ".venv")
    if not os.path.exists(venv_path):
        print("📦 Création de l'environnement virtuel...")
        run(f'"{sys.executable}" -m venv "{venv_path}"', "Impossible de créer le venv")
    else:
        print_success("✅ Venv déjà existant")
    return venv_path

def update_pip_venv(venv_path):
    """Met à jour pip, setuptools et wheel dans le venv via python -m pip"""
    python_exec = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "python3")
    print("⬆️ Mise à jour de pip, setuptools et wheel dans le venv...")
    run(f'"{python_exec}" -m pip install --upgrade pip setuptools wheel', "Mise à jour pip/setuptools/wheel échouée")

def install_requirements(project_path, venv_path):
    python_exec = os.path.join(venv_path, "Scripts", "python.exe") if platform.system() == "Windows" else os.path.join(venv_path, "bin", "python3")
    req_file = os.path.join(project_path, "requirements.txt")

    if os.path.exists(req_file):
        print("📥 Installation des dépendances du projet...")
        run(f'"{python_exec}" -m pip install -r "{req_file}"', "Installation des dépendances échouée")
    else:
        print_warn("⚠ Pas de requirements.txt trouvé, skipping installation.")

def run_project_setup(project_path, venv_path):
    system = platform.system()
    python_exec = os.path.join(venv_path, "Scripts", "python.exe") if system == "Windows" else os.path.join(venv_path, "bin", "python3")
    setup_file = os.path.join(project_path, "setup_win.py" if system == "Windows" else "setup_linux.py")

    # 🔥 Suppression de update.txt si présent
    update_file = os.path.join(project_path, "update.txt")
    if os.path.exists(update_file):
        try:
            os.remove(update_file)
            print_success("✅ Fichier update.txt supprimé")
        except Exception as e:
            print_warn(f"⚠ Impossible de supprimer update.txt : {e}")

    if os.path.exists(setup_file):
        print(f"🛠 Exécution de {os.path.basename(setup_file)} …")
        run(f'"{python_exec}" "{setup_file}"', f"Échec lors de l'exécution de {os.path.basename(setup_file)}")
    else:
        print_warn(f"⚠ {os.path.basename(setup_file)} introuvable. Ignoré.")

# ===================== SCRIPT PRINCIPAL =====================
def main():
    check_python_version()
    print("🚀 Installation automatique du projet Manga")

    folder = input("Entrez le chemin du dossier d'installation : ").strip()
    if not folder:
        print_error("❌ Chemin vide. Abandon.")
        input("Appuyez sur Entrée pour quitter...")
        return

    os.makedirs(folder, exist_ok=True)

    project_path = download_and_extract(folder)
    if not project_path:
        print_error("❌ Impossible de continuer sans projet extrait.")
        input("Appuyez sur Entrée pour quitter...")
        return

    venv_path = create_venv(project_path)
    update_pip_venv(venv_path)
    install_requirements(project_path, venv_path)
    run_project_setup(project_path, venv_path)

    print_success("✅ Installation complète. L'application est prête à être lancée.")
    input("Appuyez sur Entrée pour fermer le script...")

if __name__ == "__main__":
    main()
