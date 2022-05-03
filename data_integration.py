from pipline.PoRo import PoRo
from pipline.connection_to_GCP import *
import datetime

"""
a executerune une fois lors de la creation du projet  (injecter les données) 
pour la création de la table et pour l'insertion des projet en cours qui auront les valeurs par defauts
pour chaque piéces 
"""


create_table_big_query()

creation_projet_en_cours()

creation_projet_p1310()

creation_projet_HCB()

creation_projet_DHN()

creation_projet_P1316()
