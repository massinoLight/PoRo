from google.cloud import bigquery
#from google.cloud import storage
import requests
import configparser
import os
from pipline.PoRo import PoRo
import datetime



liste_projet_encours=["R1310","DJB","HJB2","P1317","R1312"]
liste_projet_termine=["P1310","HCB","DHN","P1316"]
pieces=["Planche de bord","Console","Panneau porte AV","Panneau porte AR","Projecteur","DRL","Feu","Sièges","Bouclier AV",
       "Bouclier AR","Miroirs extérieurs","Barres de toit","Volants","Cluster","Ecran","barette (switches)","Habillage de coffre"]

def check_proxy():
    try:
        r = requests.get('https://www.google.com')

    except requests.exceptions.RequestException as e:  # This is the correct syntax

        config = configparser.ConfigParser()
        config.read("./config.ini")
        os.environ['https_proxy'] = "http://" + config['SERVER']['proxyUser'] + config['SERVER']['proxypsw'] + config['SERVER']['proxypsw'] + config['SERVER']['proxy']
        print("Proxy:",os.environ['https_proxy'])


#Create table from bucket file to big query
def get_data_from_big_query_connection(table):
    # Construct a BigQuery client object.
    client = bigquery.Client()
    table_id = "projet-sanae.PoRo."+table


    QUERY =f"""SELECT * FROM `{table_id}` """
    query_job = client.query(QUERY)  # API request
    rows = query_job.result()  # Waits for query to finish

    for row in rows:
        print(row)

#insertion d'une ligne de PoRo
def insert_into_big_query(PoRo):

    client = bigquery.Client()
    table_id = "projet-sanae.PoRo.poroallprojetcts"

    rows_to_insert = [
        {"projet":PoRo.projet,  "piece": PoRo.piece, "Ready_to_start_PC": PoRo.Ready_to_start_PC,"PoRo_bouilding_PC_CF":PoRo.PoRo_building_PC_CF,
         "Expert_nomination":PoRo.Expert_nomination,"Expert_nomination_date":PoRo.Expert_nomination_date,"PoRo_Signature_Cf":PoRo.PoRo_Signature_Cf,
         "attribution_CF_date":PoRo.attribution_CF_date,"Poro_Achievement_CF_p":PoRo.Poro_Achievement_CF_p,"Suppluiers_Nomination":PoRo.Suppluiers_Nomination,
         "Suppluiers_Nomination_date":PoRo.Suppluiers_Nomination_date,"Description":PoRo.Description,"date_mise_a_jour":PoRo.date_mise_a_jour,"PoRo_termine":PoRo.PoRo_termine
         }
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


#Creation de la table sur GCP a executer une seul fois lors du lancement du projet
def create_table_big_query():
    # Construct a BigQuery client object.
    client = bigquery.Client()

    table_id = "projet-sanae.PoRo.poroallprojetcts"

    schema = [
        bigquery.SchemaField("projet", "STRING", mode="REQUIRED",description=" nom du projet"),
        bigquery.SchemaField("piece", "STRING", mode="REQUIRED",description=" 17 piéces:[Planche de bord,Console,Panneau porte AV,Panneau porte AR,Projecteur...]"),
        bigquery.SchemaField("Ready_to_start_PC", "INTEGER", mode="REQUIRED",description="1:ROUGE -> [@PC : Data Missing / @PC à  CF :  No PoRo convergence/ @CF : No PoRo Signature/ @>CF : Heavy modification] "),
        bigquery.SchemaField("PoRo_bouilding_PC_CF", "INTEGER", mode="REQUIRED",description="2:JAUNE-> [@PC : Data in progress/  @PC à  CF :  Work in progress / @CF : Some Signature are missing/  @>CF : light Techn. / Design / Product modification] "),
        bigquery.SchemaField("Expert_nomination", "INTEGER", description=" 3:VERT-> [OK / Done / Conform]"),
        bigquery.SchemaField("Expert_nomination_date", "DATE",description=" DATE attribution Expert_nomination "),
        bigquery.SchemaField("PoRo_Signature_Cf", "INTEGER", mode="REQUIRED", description=" 4: NOIRE/BAREE -> [COCA, morphing, or out of BOM]"),
        bigquery.SchemaField("attribution_CF_date", "DATE", description=" DATE signature CF "),
        bigquery.SchemaField("Poro_Achievement_CF_p", "INTEGER", mode="REQUIRED", description=" 5: GRIS -> [Not concerned]" ),
        bigquery.SchemaField("Suppluiers_Nomination", "INTEGER", mode="REQUIRED",description=" 1:Done ,2:todoc ,3: pas cocerne" ),
        bigquery.SchemaField("Suppluiers_Nomination_date", "DATE",description=" DATE attribution du Suppluiers_Nomination_date " ),
        bigquery.SchemaField("Description", "STRING"),
        bigquery.SchemaField("date_mise_a_jour", "DATE", mode="REQUIRED", description=" DATE de la derniere mise a jour de la ligne "),
        bigquery.SchemaField("PoRo_termine", "INTEGER", mode="REQUIRED",description=" 1 si PROCESSUS PoRo TERMINE 0 sinon"),


    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

#creation des projet sur la table avec les champs par defaut
def creation_projet_en_cours():


    for projet in liste_projet_encours:
        print(projet)
        for piece in pieces:

            p1 = PoRo(projet=projet, piece=piece, Ready_to_start_PC=5, PoRo_building_PC_CF=5, Expert_nomination=5,Expert_nomination_date=None,
                  PoRo_Signature_Cf=5,attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=5,
                  Suppluiers_Nomination_date=None,Description="",date_mise_a_jour=str(datetime.datetime.now().date()),PoRo_termine=0)
            insert_into_big_query(p1)


def creation_projet_p1310():

            p1 = PoRo(projet="P1310", piece="Planche de bord", Ready_to_start_PC=3, PoRo_building_PC_CF=3, Expert_nomination=3,Expert_nomination_date=None,
                  PoRo_Signature_Cf=3,attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=2,
                  Suppluiers_Nomination_date=None,Description="",date_mise_a_jour=str(datetime.datetime.now().date()),PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Console", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Panneau porte AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=1, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)
            p1 = PoRo(projet="P1310", piece="Panneau porte AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Projecteur", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Feu", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="DRL", Ready_to_start_PC=5, PoRo_building_PC_CF=5,
                      Expert_nomination=5, Expert_nomination_date=None,
                      PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Sièges", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=1, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="Ecart textile vs cout. Le reste de la DT n'est pas bloquant pour la nomination",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Bouclier AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Bouclier AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Miroirs extérieurs", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Barres de toit", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=2,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)


            p1 = PoRo(projet="P1310", piece="Volants", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=6,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Cluster", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=4, Suppluiers_Nomination=5,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Ecran", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=4, Suppluiers_Nomination=5,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="barette (switches)", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
                      Expert_nomination=3, Expert_nomination_date=None,
                      PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=4, Suppluiers_Nomination=5,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)

            p1 = PoRo(projet="P1310", piece="Habillage de coffre", Ready_to_start_PC=5, PoRo_building_PC_CF=5,
                      Expert_nomination=5, Expert_nomination_date=None,
                      PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=5,
                      Suppluiers_Nomination_date=None, Description="",
                      date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
            insert_into_big_query(p1)




def creation_projet_HCB():
    p1 = PoRo(projet="HCB", piece="Planche de bord", Ready_to_start_PC=4, PoRo_building_PC_CF=5, Expert_nomination=5,
              Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="", date_mise_a_jour=str(datetime.datetime.now().date()),
              PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Console", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Panneau porte AV", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None,
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)
    p1 = PoRo(projet="HCB", piece="Panneau porte AR", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Projecteur", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Feu", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=2, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="DRL", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=2, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Sièges", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=2, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Bouclier AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=2, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Bouclier AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=2, attribution_CF_date=None, Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Miroirs extérieurs", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Barres de toit",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)



    p1 = PoRo(projet="HCB", piece="Volants",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Cluster",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Ecran",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="barette (switches)", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="HCB", piece="Habillage de coffre",  Ready_to_start_PC=5, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)





def creation_projet_DHN():
    p1 = PoRo(projet="DHN", piece="Planche de bord", Ready_to_start_PC=4, PoRo_building_PC_CF=5, Expert_nomination=5,
              Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="", date_mise_a_jour=str(datetime.datetime.now().date()),
              PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Console", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Panneau porte AV", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None,
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)
    p1 = PoRo(projet="DHN", piece="Panneau porte AR", Ready_to_start_PC=4, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=str(datetime.datetime(2021, 2, 21).date()), Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description=" GW1 Modification request @ VPC (ighting, FR/RR seats, RRBumper). New PoRo update in W36, but not signed",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Projecteur", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=str(datetime.datetime(2021, 2, 21).date()), Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description=" GW1 Modification request @ VPC (ighting, FR/RR seats, RRBumper). New PoRo update in W36, but not signed",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Feu", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=str(datetime.datetime(2021, 2, 21).date()), Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description=" GW1 Modification request @ VPC (ighting, FR/RR seats, RRBumper). New PoRo update in W36, but not signed",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="DRL", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=str(datetime.datetime(2021, 2, 21).date()), Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description=" GW1 Modification request @ VPC (ighting, FR/RR seats, RRBumper). New PoRo update in W36, but not signed",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Sièges", Ready_to_start_PC=4, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Bouclier AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Bouclier AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=3, Expert_nomination_date=None,
              PoRo_Signature_Cf=3, attribution_CF_date=None, Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=None, Description="'Styling modifications since VPC/GW1 not updated in the PoRo",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Miroirs extérieurs", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Barres de toit",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)



    p1 = PoRo(projet="DHN", piece="Volants",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Cluster",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Ecran",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="barette (switches)", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="DHN", piece="Habillage de coffre",  Ready_to_start_PC=5, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)


def creation_projet_P1316():
    p1 = PoRo(projet="P1316", piece="Planche de bord", Ready_to_start_PC=3, PoRo_building_PC_CF=1, Expert_nomination=5,
              Expert_nomination_date=None,PoRo_Signature_Cf=1, attribution_CF_date=None, Poro_Achievement_CF_p=1, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()), Description="'PoRO not built because of late Design/Eng Convergence",
              date_mise_a_jour=str(datetime.datetime.now().date()),PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Console",  Ready_to_start_PC=3, PoRo_building_PC_CF=1, Expert_nomination=5,
              Expert_nomination_date=None,PoRo_Signature_Cf=1, attribution_CF_date=None, Poro_Achievement_CF_p=1, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()), Description="'PoRO not built because of late Design/Eng Convergence",
              date_mise_a_jour=str(datetime.datetime.now().date()),PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Panneau porte AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=1, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)
    p1 = PoRo(projet="P1316", piece="Panneau porte AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=1, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Projecteur",Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=3, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Feu", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=1, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="DRL", Ready_to_start_PC=3, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=1,
              Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()), Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Sièges", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Bouclier AV", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Bouclier AR", Ready_to_start_PC=3, PoRo_building_PC_CF=3,
              Expert_nomination=5, Expert_nomination_date=None,PoRo_Signature_Cf=2, attribution_CF_date=str(datetime.datetime(2021, 7, 11).date()),
              Poro_Achievement_CF_p=2, Suppluiers_Nomination=1,Suppluiers_Nomination_date=str(datetime.datetime(2021, 8, 1).date()),
              Description="Ecart Techno deco (cast forming) bloquant pour la nomination",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Miroirs extérieurs", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Barres de toit",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)



    p1 = PoRo(projet="P1316", piece="Volants",  Ready_to_start_PC=2, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Cluster",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Ecran",  Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="barette (switches)", Ready_to_start_PC=4, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)

    p1 = PoRo(projet="P1316", piece="Habillage de coffre",  Ready_to_start_PC=5, PoRo_building_PC_CF=5,
              Expert_nomination=5, Expert_nomination_date=None,
              PoRo_Signature_Cf=5, attribution_CF_date=None, Poro_Achievement_CF_p=5, Suppluiers_Nomination=3,
              Suppluiers_Nomination_date=None, Description="",
              date_mise_a_jour=str(datetime.datetime.now().date()), PoRo_termine=1)
    insert_into_big_query(p1)
