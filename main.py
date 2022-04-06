

from pipline.PoRo import PoRo
from pipline.connection_to_GCP import *
import datetime
x = datetime.datetime(2021, 10, 4).date()

p1 = PoRo(projet="R1316",piece="Planche de bord",Ready_to_start_PC=4,PoRo_building_PC_CF=5,Expert_nomination=None,PoRo_Signature_Cf=5,
          week_attribution_CF=None,Poro_Achievement_CF_p=5,Suppluiers_Nomination=5,Description="")
insert_into_big_query(p1)

p1 = PoRo(projet="R1316",piece="Console",Ready_to_start_PC=3,PoRo_building_PC_CF=3,Expert_nomination=None,PoRo_Signature_Cf=2,
          week_attribution_CF=str(x),Poro_Achievement_CF_p=3,Suppluiers_Nomination=3,Description="' - Sgnature en cours (reste APO), "
                                                                                            "ajout d'éléments thème design / produit depuis CF (stargate, coiffe, cast forming), donc update. Chiffres différents "
                                                                                            "portratit robot VS KPM, mais budget en écart à ré-évaluer au CC (idem P1310)")
insert_into_big_query(p1)
