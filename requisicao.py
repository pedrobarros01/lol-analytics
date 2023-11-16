from dotenv import load_dotenv
import os
import requests as req
import pandas as pd
import time


class Requisicao:
    def __init__(self, summonerName: str) -> None:
        
        self.__TOKEN =  os.getenv("TOKEN")
        self.server = "br1"
        self.server_original = "americas"
        self.url = f'https://{self.server}.api.riotgames.com'
        self.url_original = f'https://{self.server_original}.api.riotgames.com'
        self.summonerName = summonerName

    def __get_puuid_by_summonerName(self):
        route_puuid = f'/lol/summoner/v4/summoners/by-name/{self.summonerName}?api_key={self.__TOKEN}'
        data = req.get(self.url + route_puuid).json()
        puuid = data['puuid']
        return puuid
    
    def __get_matches_by_puuid(self) -> list[str]:
        puuid = self.__get_puuid_by_summonerName()
        route_matches = f'/lol/match/v5/matches/by-puuid/{puuid}/ids?type=ranked&count=100&api_key={self.__TOKEN}'
        data_matches = req.get(self.url_original + route_matches).json()
        return data_matches, puuid
    
    def __find_infos_game_of_player(self, match, puuid):
        infos_players = match['info']['participants']
        for info in infos_players:
            if info['puuid'] == puuid:
                return info
        return None

    def get_info_matches(self):
        data_matches, puuid = self.__get_matches_by_puuid()
        print(puuid)
        data = {
            'kills': [],
            'assists': [],
            'deaths': [],
            'kda': [],
            'wardsPlaced': [],
            'goldEarned': [],
            'magicDamageDealt': [],
            'physicalDamageDealt': [],
            'lane': [],
            'wardsKilled' : [],
            'totalDamageDealt': []
        }
        for i, match_id in enumerate(data_matches):
            route_match = f'/lol/match/v5/matches/{match_id}?api_key={self.__TOKEN}'
            match = req.get(self.url_original + route_match)
            while match.status_code == 429:
                print("Chegou no limite, bo esperar 30 seg")
                time.sleep(30)
                print("Cbo tentar dnv")
                match = req.get(self.url_original + route_match)
                
            match = match.json()
            #print(match)
            info = self.__find_infos_game_of_player(match, puuid) 
            kda = 0
            if info['deaths'] > 0:      
                kda = (info['assists'] + info['kills']) / (info['deaths'])
            else:
                kda = (info['assists'] + info['kills'])
            data['assists'].append(info['assists'])
            data['deaths'].append(info['deaths'])
            data['goldEarned'].append(info['goldEarned'])
            data['kda'].append(kda)
            data['kills'].append(info['kills'])
            data['magicDamageDealt'].append(info['magicDamageDealt'])
            data['physicalDamageDealt'].append(info['physicalDamageDealt'])
            data['lane'].append(info['lane'])
            data['totalDamageDealt'].append(info['totalDamageDealt'])
            data['wardsKilled'].append(info['wardsKilled'])
            data['wardsPlaced'].append(info['wardsPlaced'])
            print(f'{i}: kda = {kda}')
        
        df = pd.DataFrame(data)
        return df



if __name__ == '__main__':
    load_dotenv()
    requisicao = Requisicao('MastigaVinculado')
    df = requisicao.get_info_matches()
    print(df)
    df.to_csv('out.zip',index=False)






