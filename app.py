from flask import Flask, render_template, request, flash

from pipline.connection_to_GCP import modif_into_big_query, get_into_big_query

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')



@app.route('/modification', methods=['GET', 'POST'])
def modification():
    projet = request.args.get('projet')
    piece = request.args.get('piece')
    jalon = request.args.get('jalon')
    etat = request.args.get('etat')
    if jalon is not None:
        jalon=int(jalon)
        jalon=jalon % 6
    jalons = ["Ready_to_start_PC", "PoRo_building_PC_CF", "Expert_nomination", "PoRo_Signature_CF","Poro_Achievement_CF_p", "Suppluiers_Nomination"]
    print("projet="+str(projet),"piece="+str(piece),"jalon= "+str(jalon),"etat= "+str(etat))
    if request.method == 'POST':
        req = request.form

        if req.get("projet")!="" and req.get("Piece")!='' and req.get("etat")!='':
            modif_into_big_query(projet=req.get("projet"), piece=req.get("Piece"), jalon=req.get("jalon"), status=req.get("etat"), remarque=req.get("remarque"))
            print(req.get("projet"))
            print(req.get("Piece"))
            print(req.get("etat"))
            dataframe = get_into_big_query(req.get("projet"))
            descriptions = dataframe['Description'].tolist()
            weeks = dataframe[['Ready_to_start_PC_W', 'PoRo_building_PC_CF_W', 'Expert_nomination_W', 'PoRo_Signature_CF_W','Poro_Achievement_CF_p_W', 'Suppluiers_Nomination_W']].values.tolist()
            dataframe = dataframe[['Ready_to_start_PC', 'PoRo_building_PC_CF', 'Expert_nomination', 'PoRo_Signature_CF','Poro_Achievement_CF_p', 'Suppluiers_Nomination']]
            print(dataframe.values)
            couleurs = []

            for i in range(0, len(dataframe)):
                for j in range(0, len(dataframe.values[i])):
                    if dataframe.values[i][j] == 1:
                        couleurs.append("#e32014")  # red data missing
                    else:
                        if dataframe.values[i][j] == 2:
                            couleurs.append("#FFC300")  # yelow data in progress
                        else:
                            if dataframe.values[i][j] == 3:
                                couleurs.append("#7ce314")  # green ok/done/conform
                            else:
                                if dataframe.values[i][j] == 4:
                                    couleurs.append("#141514")  # black COCA ,morphing
                                else:
                                    if dataframe.values[i][j] == 5:
                                        couleurs.append("#949794")  # grey not concerned

            return render_template('visualisation.html', projet=req.get("projet"), couleurs=couleurs,descriptions=descriptions,weeks=weeks)
        else :
            bien='saisie manquante'
            return render_template('modification.html', bien=bien,projet=req.get("projet"),piece=req.get("Piece"),jalon=req.get("jalon"))



    return render_template('modification.html',projet=request.args.get('projet'),piece=piece,jalon=jalons[jalon])


"""
@app.route('/modification$projet=<projet>$piece=<piece>', methods=['GET', 'POST'])
def modification(projet,piece):
    print("projet="+str(projet),"piece="+str(piece))
    if request.method == 'POST':
        req = request.form
        if req.get("projet")!="" and req.get("Piece")!='':
            modif_into_big_query(projet=req.get("projet"), piece=req.get("Piece"), jalon=req.get("jalon"), status=req.get("etat"), remarque=req.get("remarque"))
            bien='done'
            print(req.get("projet"))
            dataframe = get_into_big_query(req.get("projet"))
            dataframe = dataframe[
                ['Ready_to_start_PC', 'PoRo_bouilding_PC_CF', 'Expert_nomination', 'PoRo_Signature_Cf',
                 'Poro_Achievement_CF_p', 'Suppluiers_Nomination']]
            print(dataframe.values)
            couleurs = []
            for i in range(0, len(dataframe)):
                for j in range(0, len(dataframe.values[i])):
                    if dataframe.values[i][j] == 1:
                        couleurs.append("#e32014")  # red data missing
                    else:
                        if dataframe.values[i][j] == 2:
                            couleurs.append("#FFC300")  # yelow data in progress
                        else:
                            if dataframe.values[i][j] == 3:
                                couleurs.append("#7ce314")  # green ok/done/conform
                            else:
                                if dataframe.values[i][j] == 4:
                                    couleurs.append("#141514")  # black COCA ,morphing
                                else:
                                    if dataframe.values[i][j] == 5:
                                        couleurs.append("#949794")  # grey not concerned

            return render_template('visualisation.html', Projet=req.get("projet"), couleurs=couleurs)
        else :
            bien='saisie manquante'
            return render_template('modification.html', bien=bien)



    return render_template('modification.html',projet=projet,piece=piece)

"""

@app.route('/visualisation/<string:projet>',methods=['GET'])
def visualisation(projet):
    print(projet)
    dataframe=get_into_big_query(projet)
    descriptions=dataframe['Description'].tolist()
    df = dataframe[['Ready_to_start_PC_W', 'PoRo_building_PC_CF_W', 'Expert_nomination_W', 'PoRo_Signature_CF_W', 'Poro_Achievement_CF_p_W','Suppluiers_Nomination_W']]
    dataframe = dataframe[['Ready_to_start_PC', 'PoRo_building_PC_CF','Expert_nomination','PoRo_Signature_CF','Poro_Achievement_CF_p','Suppluiers_Nomination']]
    print(dataframe.values)


    couleurs = []
    weeks=[]

    for i in range(0, len(dataframe)):
        for j in range(0, len(dataframe.values[i])):
            weeks.append(df.values[i][j])
            if dataframe.values[i][j] == 1:
                couleurs.append("#e32014")  # red data missing
            else:
                if dataframe.values[i][j] == 2:
                    couleurs.append("#FFC300")  # yellow data in progress
                else:
                    if dataframe.values[i][j] == 3:
                        couleurs.append("#7ce314")  # green ok/done/conform
                    else:
                        if dataframe.values[i][j] == 4:
                            couleurs.append("#141514")  # black COCA ,morphing
                        else:
                            if dataframe.values[i][j] == 5:
                                couleurs.append("#949794")  # grey not concerned
    print(weeks)
    return render_template('visualisation.html',projet=projet,couleurs=couleurs,piece='',descriptions=descriptions,weeks=weeks)

