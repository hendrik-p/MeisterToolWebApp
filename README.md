Eine kleine WebApp, welche die "Monster und Wildtiere"-Funktion von Odatas
MeisterTools (https://github.com/Odatas/MeisterTools) reproduziert.

Zum Ausprobieren am besten eine virtuelle Umgebung aufsetzen und darin Flask
installieren:
```
python3 -m venv env
. env/bin/activate
pip install Flask
pip install flask-wtf
pip install flask-mobility
```
Dann einfach die App mit `FLASK_ENV=development python app.py` starten und das
Ergebnis im Browser unter localhost:5000 bewundern. Alternativ kann man die App
auch unter http://iori.pythonanywhere.com/ anschauen.
