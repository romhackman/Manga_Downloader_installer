@echo off

REM Récupère le chemin AppData\Local
set "LOCALAPPDATA=%LOCALAPPDATA%"

REM Chemins
set "VENV=%LOCALAPPDATA%\Manga\.venv"
set "SCRIPT=%LOCALAPPDATA%\Manga\lecture.py"

REM Vérifications
if not exist "%VENV%\Scripts\python.exe" (
    echo ERREUR : Python du venv introuvable
    pause
    exit /b
)

if not exist "%SCRIPT%" (
    echo ERREUR : lecture.py introuvable
    pause
    exit /b
)

REM Lancement du script avec le python du venv
"%VENV%\Scripts\python.exe" "%SCRIPT%"
