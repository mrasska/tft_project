import json
import requests
import pdb
import pandas as pd
import time

url_gm='https://euw1.api.riotgames.com/tft/league/v1/grandmaster'


header={
    
}

def connect(url, header): 
    req=requests.get(url=url, headers=header)
    req=req.json()
    return req

def crawl_json(req):
    player=[]
    win_player=[]
    losses_player=[]
    rank=[]

    for m in range(len(req['entries'])):
        v=req['entries'][m]['summonerName']
        player.append(v)

        w=req['entries'][m]['wins']
        win_player.append(w)

        d=req['entries'][m]['losses']
        losses_player.append(d)

    return player, win_player, losses_player

def db_player(db): 
    data={'name_player':db[0], 'total_ranked_win_season': db[1], 'total_ranked_losses_season': db[2]}
    df_db=pd.DataFrame(data)
    return df_db

def get_puid(df_db, header): 
    name_player=df_db['name_player']
    name_player=name_player.to_list()

    puid=[]
    for m in name_player:
        url_puid='https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/'+m
        req=connect(url_puid, header)
        print(m)
        try :
            p=req['puuid']
            puid.append(p)
        except KeyError : 
            pdb.set_trace()
        time.sleep(2)
    
    df_db['puid']=puid
    return df_db

def type_db(header):
    user_value=input("For which rank would you like to get the data? Type C for Challenger / GM for Grand Master : ")

    #URLS to request to Riot API
    url_c='https://euw1.api.riotgames.com/tft/league/v1/challenger'
    url_gm='https://euw1.api.riotgames.com/tft/league/v1/grandmaster'
    url_m='https://euw1.api.riotgames.com/tft/league/v1/master'

    if user_value=='C':
        req=connect(url_c, header)
        db=crawl_json(req)
        name='leaderboard_chall.csv'
        df_db=db_player(db)
        df_db=get_puid(df_db=df_db, header=header)
        df_db.to_csv(name, header=True, index=False)

    elif user_value=='GM':
        req=connect(url_gm, header)
        db=crawl_json(req)
        name='leaderboard_gm.csv'
        df_db=db_player(db)
        df_db=get_puid(df_db=df_db, header=header)
        df_db.to_csv(name, header=True, index=False)

    return print('Data collected!'), df_db

df_db=type_db(header)
pdb.set_trace()