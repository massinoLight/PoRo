class PoRo:
  def __init__(poro,projet, piece, Ready_to_start_PC,PoRo_building_PC_CF,
               Expert_nomination,Expert_nomination_date,PoRo_Signature_Cf,
               attribution_CF_date,Poro_Achievement_CF_p,Suppluiers_Nomination,Suppluiers_Nomination_date,
               Description,date_mise_a_jour,PoRo_termine):
    poro.projet = projet
    poro.piece = piece
    poro.Ready_to_start_PC = Ready_to_start_PC
    poro.PoRo_building_PC_CF = PoRo_building_PC_CF
    poro.Expert_nomination = Expert_nomination
    poro.Expert_nomination_date = Expert_nomination_date
    poro.PoRo_Signature_Cf = PoRo_Signature_Cf
    poro.attribution_CF_date = attribution_CF_date
    poro.Poro_Achievement_CF_p = Poro_Achievement_CF_p
    poro.Suppluiers_Nomination = Suppluiers_Nomination
    poro.Suppluiers_Nomination_date = Suppluiers_Nomination_date
    poro.Description = Description
    poro.date_mise_a_jour = date_mise_a_jour
    poro.PoRo_termine = PoRo_termine

    """ def date_toweek(poro,date):
      week = date.isocalendar()[1]
      if week / 10 < 1:
          week = "0" + str(week)
      year = str(date.isocalendar()[0])[2: 4: 1]
      final = "W" + year + str(week)
      poro.week_attribution_CF=final
      return final
"""






