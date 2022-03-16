import json
import requests
import pdb
import pandas as pd


url_gm='https://euw1.api.riotgames.com/tft/league/v1/grandmaster'
url_m='https://euw1.api.riotgames.com/tft/league/v1/master'

header={
    "User-Agent": "",
    "Accept-Language": "",
    "Accept-Charset": "",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": ""
    }

def connect(url, header): 
    req=requests.get(url=url, headers=header)
    req=req.json()
    return req

def crawl_json(req):
    id_player=[]
    win_player=[]
    losses_player=[]
    rank=[]

    for m in range(len(req['entries'])):
        v=req['entries'][m]['summonerId']
        id_player.append(v)

        w=req['entries'][m]['wins']
        win_player.append(m)

        d=req['entries'][m]['losses']
        losses_player.append(d)

    return id_player, win_player, losses_player

def db_player(db_master, db_gm): 
    data_master={'id_player':db_master[0], 'total_ranked_win_season': db_master[1], 'total_ranked_losses_season': db_master[2]}
    df_master=pd.DataFrame(data_master)

    data_gm={'id_player':db_gm[0], 'total_ranked_win_season': db_gm[1], 'total_ranked_losses_season': db_gm[2]}
    df_gm=pd.DataFrame(data_gm)

    df_db=df_gm.append(df_master, ignore_index=True)

    return df_db

def launch_process(url_gm, url_m, header): 
    req_m=connect(url_m,header)
    db_m=crawl_json(req=req_m)

    req_gm=connect(url_gm, header)
    db_gm=crawl_json(req=req_gm)

    df_db_player=db_player(db_master=db_m, db_gm=db_gm)

    #optional to save the DB as CSV
    df_db_player.to_csv('db_players.csv', header=True, index=False)

    return print('Data collected!')

launch_process(url_gm=url_gm, url_m=url_m, header=header)