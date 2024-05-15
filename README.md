Plateforme de réservation de places à des compétitions.

## Initialisation du projet

### Windows :
```
git clone https://github.com/Bonin-Alexandre/Reservation.git

cd Reservation 
python -m venv env 
env\Scripts\activate

pip install -r requirements.txt
```

### MacOS et Linux :
```
git clone https://github.com/Bonin-Alexandre/Reservation.git

cd Reservation 
python3 -m venv env 
source env/bin/activate

pip install -r requirements.txt
```


## Utilisation

1. Lancer le serveur Flask :

```
$env:FLASK_APP = "server.py"
flask run
```

2. Pour accéder au site, se rendre sur l'adresse par défaut : [http://127.0.0.1:5000/](http://127.0.0.1:5000/) !
