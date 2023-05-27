# Nom du fichier: dao.py
#
# Ce fichier contient les fonctionnalités de création et de gestion de notre base de données sqlite3.
#
# Auteurs: Patrice Gallant et Roberto Nightingale

import sqlite3
from datetime import datetime

BD = "fourier_db"

FK_ON = 'PRAGMA foreign_keys = 1'
FK_OFF = 'PRAGMA foreign_keys = 0'

# ----------------------------------------------------------------------------------------------------------------------
CREATE_DESSINS_FAVORIS = '''
CREATE TABLE IF NOT EXISTS dessins_favoris (
    id INTEGER NOT NULL PRIMARY KEY,
    usager INTEGER NOT NULL,
    dessin INTEGER NOT NULL,
    date VARCHAR NOT NULL
)
'''
DROP_DESSINS_FAVORIS = 'DROP TABLE IF EXISTS dessins_favoris'
INSERT_DESSINS_FAVORIS = 'INSERT INTO dessins_favoris(usager,dessin, date) VALUES(?,?, ?)'
SELECT_DESSINS_FAVORIS = 'SELECT * FROM dessins_favoris'

# ----------------------------------------------------------------------------------------------------------------------

CREATE_DESSINS = '''
CREATE TABLE IF NOT EXISTS dessins (
    id INTEGER NOT NULL PRIMARY KEY,
    nom VARCHAR NOT NULL,
    svg VARCHAR NOT NULL,
    date VARCHAR NOT NULL
)
'''
DROP_DESSINS = 'DROP TABLE IF EXISTS dessins'
INSERT_DESSINS = 'INSERT INTO dessins(nom,svg, date) VALUES(?,?, ?)'
SELECT_DESSINS = 'SELECT * FROM dessins'
# ----------------------------------------------------------------------------------------------------------------------

CREATE_USAGERS = '''
CREATE TABLE IF NOT EXISTS usagers (
    id INTEGER NOT NULL PRIMARY KEY,
    username VARCHAR NOT NULL,
    password VARCHAR NOT NULL
)
'''
DROP_USAGERS = 'DROP TABLE IF EXISTS usagers'
INSERT_USAGERS = 'INSERT INTO usagers(username,password) VALUES(?,?)'
SELECT_USAGERS = 'SELECT * FROM usagers'

# ----------------------------------------------------------------------------------------------------------------------
CREATE_PREFERENCES = '''
CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER NOT NULL PRIMARY KEY,
    user INTEGER NOT NULL,
    background_color INTEGER NOT NULL,
    arrows_color INTEGER NOT NULL,
    circles_color INTEGER NOT NULL,
    drawing_color INTEGER NOT NULL
)
'''
DROP_PREFERENCES = 'DROP TABLE IF EXISTS preferences'
INSERT_PREFERENCES = '''INSERT INTO preferences(user,background_color, arrows_color, circles_color, drawing_color) 
                     VALUES(?,?)'''
SELECT_PREFERENCES = 'SELECT * FROM preferences'

# ----------------------------------------------------------------------------------------------------------------------
CREATE_AUTEURS_FAVORIS = '''
CREATE TABLE IF NOT EXISTS auteurs_favoris (
    id INTEGER NOT NULL PRIMARY KEY,
    user INTEGER NOT NULL,
    autor INTEGER NOT NULL
)
'''
DROP_AUTEURS_FAVORIS = 'DROP TABLE IF EXISTS auteurs_favoris'
INSERT_AUTEURS_FAVORIS = 'INSERT INTO auteurs_favoris(user, autor) VALUES(?,?)'
SELECT_AUTEURS_FAVORIS = 'SELECT * FROM auteurs_favoris'


# ----------------------------------------------------------------------------------------------------------------------

class DAO:
    def __init__(self, chemin=BD):
        self.chemin = chemin
        self.curseur = None
        self.connexion = None

    def connecter(self):
        self.connexion = sqlite3.connect(self.chemin)
        self.curseur = self.connexion.cursor()
        self.curseur.execute(FK_ON)

    def deconnecter(self):
        self.curseur.close()
        self.connexion.close()

    def creer_tables(self):
        self.curseur.execute(CREATE_USAGERS)
        self.curseur.execute(CREATE_DESSINS)
        self.curseur.execute(CREATE_PREFERENCES)
        self.curseur.execute(CREATE_AUTEURS_FAVORIS)
        self.curseur.execute(CREATE_DESSINS_FAVORIS)

    def reset_tables(self):
        self.curseur.execute(DROP_USAGERS)
        self.curseur.execute(DROP_DESSINS)
        self.curseur.execute(DROP_PREFERENCES)
        self.curseur.execute(DROP_AUTEURS_FAVORIS)
        self.curseur.execute(DROP_DESSINS_FAVORIS)

    def insert_usagers(self, username, password):
        self.curseur.execute(INSERT_USAGERS, (username, password))
        self.connexion.commit()

    def insert_dessins(self, nom, svg):
        self.curseur.execute(INSERT_DESSINS, (nom, svg, datetime.now()))
        self.connexion.commit()

    def insert_preferences(self, user, background_color, arrows_color, circles_color, drawing_color):
        self.curseur.execute(INSERT_PREFERENCES, (user, background_color, arrows_color, circles_color, drawing_color))
        self.connexion.commit()

    def insert_auteurs_favoris(self, user, autor):
        self.curseur.execute(INSERT_AUTEURS_FAVORIS, (user, autor))
        self.connexion.commit()

    def insert_dessins_favoris(self, usager, dessin):
        self.curseur.execute(INSERT_DESSINS_FAVORIS, (usager, dessin))
        self.connexion.commit()

    def select_usagers(self):
        self.curseur.execute(SELECT_USAGERS)
        return self.curseur.fetchall()

    def select_dessins(self):
        self.curseur.execute(SELECT_DESSINS)
        return self.curseur.fetchall()

    def select_preferences(self):
        self.curseur.execute(SELECT_PREFERENCES)
        return self.curseur.fetchall()

    def select_auteurs_favoris(self):
        self.curseur.execute(SELECT_AUTEURS_FAVORIS)
        return self.curseur.fetchall()

    def select_dessins_favoris(self):
        self.curseur.execute(SELECT_DESSINS_FAVORIS)
        return self.curseur.fetchall()
