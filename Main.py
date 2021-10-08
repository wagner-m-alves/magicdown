from PandaFiles import Scraper
from Scan import ComandoTorrentsOrg
from Content import Serie, Session


def __ListSessions():
    Obj_Series = Serie()
    Obj_Session = Session()

    Series = Obj_Series.Load()
    Response = []

    for S in Series:
        Sessions = Obj_Session.Load(S)
        Response += Sessions

    return Response


def CheckAll():
    CheckList = __ListSessions()
    Obj_Source = ComandoTorrentsOrg()
    Obj_Session = Session()

    for Item in CheckList:
        Seriee = Item.split('.')[0]
        Temporada = Item.split('.')[1].replace('S', '')

        print(f'\n--------------------------- {Seriee} ---------------------------')
        Links = Obj_Source.GetMagneticLinks(Seriee, Temporada)
        Obj_Session.AddNewEpisodeLink(Seriee, Temporada, Links)
        print(f'--------------------------- {Seriee} ---------------------------')

    Obj_Source.CloseBrowser()



# PRINCIPAL
'''Bot = Scraper()
Bot.Run()'''

CheckAll()