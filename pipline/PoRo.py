class PoRo:
  def __init__(poro,projet, piece, Ready_to_start_PC,PoRo_building_PC_CF,
               Expert_nomination,PoRo_Signature_Cf,week_attribution_CF,Poro_Achievement_CF_p,Suppluiers_Nomination,Description):
    poro.projet = projet
    poro.piece = piece
    poro.Ready_to_start_PC = Ready_to_start_PC
    poro.PoRo_building_PC_CF = PoRo_building_PC_CF
    poro.Expert_nomination = Expert_nomination
    poro.PoRo_Signature_Cf = PoRo_Signature_Cf
    poro.week_attribution_CF = week_attribution_CF
    poro.Poro_Achievement_CF_p = Poro_Achievement_CF_p
    poro.Suppluiers_Nomination = Suppluiers_Nomination
    poro.Description = Description

    """ def date_toweek(poro,date):
      week = date.isocalendar()[1]
      if week / 10 < 1:
          week = "0" + str(week)
      year = str(date.isocalendar()[0])[2: 4: 1]
      final = "W" + year + str(week)
      poro.week_attribution_CF=final
      return final
"""






