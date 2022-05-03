class PoRo:
  def __init__(poro,projet, piece,
               Ready_to_start_PC,Ready_to_start_PC_W,
               PoRo_building_PC_CF,PoRo_building_PC_CF_W,
               Expert_nomination,Expert_nomination_W,
               PoRo_Signature_CF,PoRo_Signature_CF_W,
               Poro_Achievement_CF_p,Poro_Achievement_CF_p_W,
               Suppluiers_Nomination,Suppluiers_Nomination_W,
               Description,date_mise_a_jour,PoRo_termine):
    poro.projet = projet
    poro.piece = piece
    poro.Ready_to_start_PC = Ready_to_start_PC
    poro.Ready_to_start_PC_W = Ready_to_start_PC_W

    poro.PoRo_building_PC_CF = PoRo_building_PC_CF
    poro.PoRo_building_PC_CF_W = PoRo_building_PC_CF_W

    poro.Expert_nomination = Expert_nomination
    poro.Expert_nomination_W = Expert_nomination_W

    poro.PoRo_Signature_CF = PoRo_Signature_CF
    poro.PoRo_Signature_CF_W = PoRo_Signature_CF_W

    poro.Poro_Achievement_CF_p = Poro_Achievement_CF_p
    poro.Poro_Achievement_CF_p_W = Poro_Achievement_CF_p_W

    poro.Suppluiers_Nomination = Suppluiers_Nomination
    poro.Suppluiers_Nomination_W = Suppluiers_Nomination_W
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






