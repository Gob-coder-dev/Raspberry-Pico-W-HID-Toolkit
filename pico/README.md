# Pico HID

Cette partie transforme un Raspberry Pi Pico W en clavier USB HID pour lancer automatiquement des actions sur un PC Windows. Le script utilise la boite `Executer` de Windows (`Win + R`) pour taper des commandes, ouvrir un lien web ou telecharger un PDF.

## Ce que fait le projet

Quand le Pico demarre :

- la LED integree clignote pendant l'initialisation USB ;
- le Pico attend que Windows detecte correctement le clavier HID ;
- il lit l'etat des broches `GP0` a `GP4` ;
- il execute l'action associee a chaque broche qui est a l'etat haut.

Les conditions sont independantes : si plusieurs broches sont actives au demarrage, plusieurs actions peuvent s'enchainer.

## Materiel utilise

- Raspberry Pi Pico W
- Cable micro-USB
- Fils Dupont
- Une resistance de pull-down par entree si necessaire dans votre montage

![image1](https://github.com/user-attachments/assets/2eda4abf-9943-4d0f-996c-f3f7a612090e)
![image2](https://github.com/user-attachments/assets/59bde83e-e670-4c38-8761-3cdb4eb2a399)

## Installation sur le Pico

1. Flasher CircuitPython : maintenir `BOOTSEL`, brancher le Pico, puis copier `adafruit-circuitpython-raspberry_pi_pico_w-fr-10.0.3.uf2` sur le lecteur `RPI-RP2`.
2. Copier `boot.py` et `code.py` a la racine de `CIRCUITPY`.
3. Copier le dossier `lib` a la racine de `CIRCUITPY`.
4. Ejecter proprement le lecteur puis redemarrer le Pico.

## Broches et actions

- `GP0` : arret immediat de Windows avec `shutdown /s /t 0`.
- `GP1` : ouvre Microsoft Edge avec l'URL definie dans `code.py`.
- `GP2` : telecharge un PDF dans `%USERPROFILE%\Downloads\p.pdf`.
- `GP3` : telecharge ce meme PDF puis l'ouvre avec l'application PDF par defaut.
- `GP4` : cree un fichier texte `m.txt` dans `%TEMP%`, puis l'envoie au serveur web configure dans `code.py`.
- `GP15` : gere dans `boot.py`. Si `GP15` n'est pas a l'etat haut au boot, le stockage USB `CIRCUITPY` est desactive.

## Fonctions de `code.py`

### `init_input(pin)`

Configure une broche en entree avec une resistance pull-down interne. Cela permet d'avoir un etat bas stable tant que la broche n'est pas forcee a `3V3`.

### `blink_task(stop_event, period=0.15)`

Fait clignoter la LED integree tant que l'evenement `stop_event` n'a pas ete declenche. Cette tache tourne en parallele pendant l'initialisation.

### `shutdown(kbd, layout, time_shutdown=0)`

Ouvre la fenetre `Executer`, tape la commande `shutdown /s /t ...`, puis valide. Par defaut, l'arret est immediat.

### `launch_weblink(kbd, layout, url)`

Ouvre la fenetre `Executer`, tape `msedge <url>`, puis lance Microsoft Edge sur l'adresse passee en parametre.

### `pdf_download(kbd, layout)`

Ouvre la fenetre `Executer`, puis lance une commande `cmd` qui :

- se place dans le dossier `Downloads` de l'utilisateur ;
- telecharge le PDF configure ;
- l'enregistre sous le nom `p.pdf`.

### `pdf_download_and_open(kbd, layout)`

Fait la meme chose que `pdf_download()`, puis ouvre le fichier telecharge avec l'application par defaut de Windows.

### `import_data_on_website(kbd, layout)`

Cree un fichier texte local avec `cmd`, puis l'envoie au serveur Flask via `curl`.

### `main()`

Fonction principale du script :

- demarre le clignotement de la LED ;
- attend que l'USB soit pret ;
- initialise le clavier HID et le layout AZERTY ;
- verifie les broches `GP0` a `GP4` ;
- execute les actions correspondantes ;
- arrete le clignotement, puis reste en attente.

## Remarques utiles

- Le script suppose que le PC cible accepte un clavier USB HID sans interaction supplementaire.
- Les commandes sont tapees comme si un vrai clavier etait connecte.
- Le layout utilise est prevu pour Windows FR (`keyboard_layout_win_fr.py`).
- Les URLs et noms de fichiers sont definis en dur dans `code.py` et peuvent etre modifies facilement.
