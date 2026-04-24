# Raspberry Pico W HID Toolkit

Toolkit educatif autour du Raspberry Pi Pico W utilise comme clavier USB HID sur Windows.

Le projet contient deux parties :

- `pico/` : code CircuitPython a copier sur le Pico W.
- `web/` : petit serveur Flask capable de recevoir et stocker des PDF envoyes par une commande `curl`.

## Structure

```text
.
├── pico/
│   ├── boot.py
│   ├── code.py
│   ├── lib/
│   └── README.md
├── web/
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── uploads/
│   └── README.md
├── .gitignore
└── README.md
```

## Usage

Consultez les README dedies :

- [pico/README.md](pico/README.md) pour installer et utiliser le script HID sur le Pico.
- [web/README.md](web/README.md) pour lancer le serveur Flask et recevoir les fichiers.

## Note

Ce projet est prevu pour des demonstrations educatives sur votre propre machine ou dans un environnement autorise. Les actions HID sont executees comme si un clavier physique tapait les commandes.
