Set shell = CreateObject("WScript.Shell")

' Récupère le chemin AppData\Local
localAppData = shell.ExpandEnvironmentStrings("%LOCALAPPDATA%")

' Chemins
venvActivate = """" & localAppData & "\Manga\.venv\Scripts\activate.bat"""
scriptPython = """" & localAppData & "\Manga\lecture.py"""

' Commande CMD
cmd = "cmd /c call " & venvActivate & " && python " & scriptPython

' Lancement (0 = fenêtre cachée, False = ne pas attendre)
shell.Run cmd, 0, False
