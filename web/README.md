# Web Upload

Petit serveur Flask minimaliste pour recevoir des PDF ou TXT envoyes avec `curl`.

## Fonctionnement

- `GET /` affiche un formulaire d'upload et la liste des fichiers recus.
- `POST /upload` recoit un fichier dans le champ `file`.
- `GET /files/<nom>` ouvre ou telecharge un fichier stocke.
- Les fichiers sont stockes dans `uploads/`.
- Seuls les fichiers `.pdf` et `.txt` sont acceptes.

Les fichiers recus sont prefixes par un timestamp pour eviter d'ecraser un ancien upload.

## Lancer en local

Depuis le dossier `web/` :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Le site sera disponible sur :

```text
http://127.0.0.1:5000
```

## Upload avec curl

Depuis le dossier qui contient le fichier :

```powershell
curl -F "file=@p.pdf" http://127.0.0.1:5000/upload
```

Exemple avec un fichier texte :

```powershell
curl -F "file=@m.txt" http://127.0.0.1:5000/upload
```

Depuis une autre machine du reseau, remplacez `127.0.0.1` par l'adresse IP du PC qui lance Flask.

## Token optionnel

Pour demander un token d'upload :

```powershell
$env:UPLOAD_TOKEN="demo123"
python app.py
```

Puis uploader avec :

```powershell
curl -H "X-Upload-Token: demo123" -F "file=@p.pdf" http://127.0.0.1:5000/upload
```

## Docker

Construire l'image :

```powershell
docker build -t pico-upload-site .
```

Lancer le conteneur :

```powershell
docker run --rm -p 5000:5000 -v "${PWD}/uploads:/app/uploads" pico-upload-site
```

Avec un token :

```powershell
docker run --rm -p 5000:5000 -e UPLOAD_TOKEN=demo123 -v "${PWD}/uploads:/app/uploads" pico-upload-site
```
