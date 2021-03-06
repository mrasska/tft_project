import json
import re
import requests
import pdb
import pandas as pd
import time

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

def get_puid_id(df_db, header, name): 
    name_player=df_db['name_player']
    name_player=name_player.to_list()

    puid=[]
    puuid=[]
    id_match=[]
    for m in name_player:
        url_puid='https://euw1.api.riotgames.com/tft/summoner/v1/summoners/by-name/'+m
        req=connect(url_puid, header)

        #database df_db -> players, wins, losses
        #database df_matches -> player, id_match        
        try :
            p=req['puuid']
            puid.append(p)
            
            #creating df_matches
            url_id_match='https://europe.api.riotgames.com/tft/match/v1/matches/by-puuid/'+p+'/ids?count=50'
            req_m=connect(url_id_match, header)

            for i in req_m : 
                puuid.append(p)
                id_match.append(i)

        except KeyError : 
            pdb.set_trace()
        time.sleep(2)
    
    df_db['puid']=puid

    data={'puid':puuid, 'id_match': id_match}
    df_match=pd.DataFrame(data)
    df_match.to_csv(name, header=True, index=False)
    
    return df_db, df_match




def type_db(header):
    user_value=input("For which rank would you like to get the data? Type C for Challenger / GM for Grand Master : ")

    #URLS to request to Riot API
    url_c='https://euw1.api.riotgames.com/tft/league/v1/challenger'
    url_gm='https://euw1.api.riotgames.com/tft/league/v1/grandmaster'

    if user_value=='C':
        req=connect(url_c, header)
        db=crawl_json(req)
        df_db=db_player(db)
        name_db_match='list_match_chall.csv'
        df_db=get_puid_id(df_db=df_db, header=header, name=name_db_match)
        name='leaderboard_chall.csv'
        df_db.to_csv(name, header=True, index=False)

    elif user_value=='GM':
        req=connect(url_gm, header)
        db=crawl_json(req)
        df_db=db_player(db)
        name_db_match='list_match_gm.csv'
        df_db=get_puid_id(df_db=df_db, header=header, name=name_db_match)
        name='leaderboard_gm.csv'
        df_db.to_csv(name, header=True, index=False)

    return print('Data collected!'), df_db

df_db=type_db(header)   