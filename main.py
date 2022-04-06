

from pipline.PoRo import PoRo
from pipline.connection_to_GCP import *
import datetime


p1 = PoRo(projet="R1316",piece="Planche de bord",Ready_to_start_PC=4,PoRo_building_PC_CF=5,Expert_nomination=None,PoRo_Signature_Cf=5,
          week_attribution_CF=None,Poro_Achievement_CF_p=5,Suppluiers_Nomination=5,Description="Description")
insert_into_big_query(p1)

p1 = PoRo(projet="R1316",piece="Console",Ready_to_start_PC=3,PoRo_building_PC_CF=3,Expert_nomination=None,PoRo_Signature_Cf=2,
          week_attribution_CF=None,Poro_Achievement_CF_p=5,Suppluiers_Nomination=5,Description="Description")
insert_into_big_query(p1)
