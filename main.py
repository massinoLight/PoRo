

from pipline.PoRo import PoRo
from pipline.connection_to_GCP import *









dataframe=get_into_big_query('P1310')
couleurs=[]
#dataframe = dataframe[['Ready_to_start_PC', 'PoRo_bouilding_PC_CF','Expert_nomination','PoRo_Signature_Cf','Poro_Achievement_CF_p','Suppluiers_Nomination','Description']]
print(dataframe['Description'].tolist())

