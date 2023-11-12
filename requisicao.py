from dotenv import load_dotenv
import os
import requests as req
load_dotenv()

TOKEN =  os.getenv("TOKEN")
summonerName = "MastigaVinculado"
server = "br1"
url_puuid = f'https://{server}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summonerName}?api_key={TOKEN}'
data = req.get(url_puuid).json()
puuid = data['puuid']
