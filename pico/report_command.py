# Configuration du rapport
REPORT_PATH = "%TEMP%\\rapport_demo.txt"
WEB_UPLOAD_URL = "http://10.37.79.100:5000/upload"

# Commandes organisées par sections (titre, commande, temps d'attente)
REPORT_COMMANDS = [
    ("SYSTEME", 
     'systeminfo | findstr /C:"Nom de l" /C:"OS Name" /C:"OS Version" /C:"BIOS Version" /C:"Domain" /C:"Mémoire physique totale"', 
     6.0),
     
     ("ANTIVIRUS", 
     '(powershell -NoProfile -Command "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct")', 
     1.0),
     
    ("ANTIVIRUS (Windows Defender)", 
     '(powershell -NoProfile -Command "Get-MpComputerStatus | Out-String; Get-MpPreference | Out-String")', 
     1.0),
     
    ("MAJ", 
     '(powershell -NoProfile -Command "Get-HotFix | Sort-Object InstalledOn -Descending | Select-Object -First 20")', 
     1.0),
     
    ("UTILISATEURS LOCAUX", 
     'net user', 
     1.0),
     
    ("CONFIGURATION RESEAU", 
     'ipconfig', 
     1.0),
     
    ("IP", 
     '(powershell -NoProfile -Command "Get-NetIPConfiguration | Out-String")', 
     2.0),
     
    ("MAC", 
     'getmac /v', 
     1.0),
     
    ("DNS", 
     '(powershell -NoProfile -Command "Get-DnsClientServerAddress | Out-String")', 
     2.0),
     
    ("FIREWALL", 
     '(powershell -NoProfile -Command "Get-NetFirewallProfile | Out-String")', 
     2.0),
     
    ("PARTITION ET VOLUMES", 
     'wmic logicaldisk get name,description,filesystem,size,freespace | more', 
     2.0),
     
    ("BIOS UEFI", 
     'wmic bios get manufacturer,name,version,serialnumber,releasedate | more', 
     2.0),
     
    ("CARTE MERE", 
     'wmic baseboard get product,manufacturer,version,serialnumber | more', 
     2.0),
     
    ("RAM", 
     'wmic memorychip get capacity,speed,manufacturer,partnumber | more & (powershell -NoProfile -Command "[Math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB, 2)")', 
     2.0),
     
    ("CPU", 
     'wmic cpu get name,numberofcores,numberoflogicalprocessors,maxclockspeed | more', 
     2.0),
     
    ("GPU", 
     'wmic path win32_VideoController get name,adapterram,driverversion | more', 
     2.0),
     
    ("STOCKAGE", 
     'wmic diskdrive get model,size,serialnumber,mediatype | more', 
     2.0),

    ("TASK", 
     'tasklist /svc', 
     2.0)
]