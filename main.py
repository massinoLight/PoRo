


import re
line="S37 -' $En attente de la nouvelle proposition Design suite à décision #1 S39 - Dissusion de la nouvelle Num Design." \
     " En attente de l'analyse Technique pour S43 puis reconstruction PoRo.W50: MAJ' suite à choix design, partage en W50," \
     " signature en cours."
line = re.sub("['!@#${}]", '', line)

print(line)