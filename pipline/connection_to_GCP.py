from google.cloud import bigquery
#from google.cloud import storage
import requests
import configparser
import os


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
        {"projet":PoRo.projet,"piece": PoRo.piece, "Ready_to_start_PC": PoRo.Ready_to_start_PC,"PoRo_bouilding_PC_CF":PoRo.PoRo_building_PC_CF,
         "Expert_nomination":PoRo.Expert_nomination,"PoRo_Signature_Cf":PoRo.PoRo_Signature_Cf,"week_attribution_CF":PoRo.week_attribution_CF,
         "Poro_Achievement_CF_p":PoRo.Poro_Achievement_CF_p,"Suppluiers_Nomination":PoRo.Suppluiers_Nomination,"Description":PoRo.Description
         }
    ]

    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


#Creation de nouveau projet
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
        bigquery.SchemaField("PoRo_Signature_Cf", "INTEGER", mode="REQUIRED", description=" 4: NOIRE/BAREE -> [COCA, morphing, or out of BOM]"),
        bigquery.SchemaField("week_attribution_CF", "DATE", description=" DATE signature CF "),
        bigquery.SchemaField("Poro_Achievement_CF_p", "INTEGER", mode="REQUIRED", description=" 5: GRIS -> [Not concerned]" ),
        bigquery.SchemaField("Suppluiers_Nomination", "INTEGER", mode="REQUIRED" ),
        bigquery.SchemaField("Description", "STRING"),


    ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)  # Make an API request.
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )



