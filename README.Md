# Description:  
Le programme **remplissage_attestation_deplacement.py** a pour but **unique** de faciliter le remplissage électronique de l'attestation de déplacement fournie par le gouvernement.   

## Etape n°1:  
Création d'un environnement virtuel (par exemple avec l'outil virtualenvwrapper):
```bash
mkvirtualenv --python=/usr/bin/python3.6 remplissage_attestation_deplacement
```

## Etape n°2:  
Installation des paquets dans l'environnement virtuel.
```bash
pip3 install -r requirements.txt
```

## Etape n°3:  
Modifier le fichier **conf.yaml** avec vos informations personnelles.  
Exécution du programme pour génerer une attestation:
```python3
python3 remplissage_attestation_deplacement.py motif
```
L'argument **motif** peut prendre les valeurs suivantes: **travail**, **course**, **santé**, **famille** et **sport**.  
Pour générer une attestation pour le travail:
```python3
python3 remplissage_attestation_deplacement.py travail
```
NB: La taille de l'image de la signature peut être changée avec l'outil [ImageMagick](https://imagemagick.org/script/convert.php).  
NB: Le fond de l'image de la signature peut être changé avec l'outil [GIMP](https://www.gimp.org/).

# Translation (English):
The only goal of the program **remplissage_attestation_deplacement.py** is to make easy the electronic filling of "attestation de déplacement" provided by the government.

## Step n°1:  
Creation of a virtual environment (for example by using virtualenvwrapper):
```bash
mkvirtualenv --python=/usr/bin/python3.6 remplissage_attestation_deplacement
```

## Step n°2:  
Packages installation in the virtual environment.
```bash
pip3 install -r requirements.txt
```

## Step n°3:  
Modify the configuration file **conf.yaml** with your personnal information.  
Execution of the program to generate an attestation:
```python3
python3 remplissage_attestation_deplacement.py motif
```
The argument **motif** can be replaced by the following values: **travail**, **course**, **santé**, **famille** et **sport**.  
To generate an attestation for working:  
```python3
python3 remplissage_attestation_deplacement.py travail
```
NB: Resizing of the image signature can be done with the software [ImageMagick](https://imagemagick.org/script/convert.php).  
NB: The background of the image signature can be changed with the software [GIMP](https://www.gimp.org/).