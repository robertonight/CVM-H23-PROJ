# C'est fou. Riez!

Par Roberto Nightingale et Patrice Gallant

### Sommaire:
Notre programme permet aux utilisateurs de faire des dessins continus qui sont ensuite analysés par un algorithme de 
transformée de Fourier et recréés à partir des coefficients obtenus, représentés sous forme de vecteurs dans un plan 
cartésien.

### Installation:
Utilisez cette commande pour installer les prérequis.

```sh
pip install -r requirements.txt
```

### Utilisation:

Pour démarrer l'application, il faut ouvrir un invite de commandes, se rendre au dossier contenant le projet avec la 
commande ``` cd ```
suivi de son chemin comme suit:
```commandline
cd .../CVM-H23-PROJ/dev
```
Une fois que c'est fait, exécutez la commande suivante avec le fichier main.py pour lancer le programme.
```commandline
py main.py
```

Le fichier main et les fichiers qui commencent par gui_ sont les fichiers d'interface, la vue.

Le fichier model et vector_manager sont les fichiers du modèle.

Le fichier fourier_db contient la base de données sqlite3.

L'interface se contrôle complètement avec la souris.


### Références:

Les références de stackoverflow sont précédés de ref dans les commentaires dans le code.

Grant Sanderson - https://www.3blue1brown.com/

https://stackoverflow.com/questions/27508552/pyqt-mouse-hovering-on-a-qpushbutton

https://stackoverflow.com/questions/16662638/how-to-draw-a-line-at-angle-in-qt

https://stackoverflow.com/questions/7351493/how-to-add-border-around-qwidget

### Remerciments:
Nous tenons à remercier les professeurs du département de mathématiques et du SIGMA pour nous avoir aidé à comprendre les concepts nécéssaires à la bonne intégration des séries complexes de Fourier dans notre projet.