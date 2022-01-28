import api_key
import requests
import csv

chosenUsers = list(
    ["RAFIYO", "BraDeLeOh", "HydraSniper", "EddyDev", "M1dus", "KimJxngUn", "Young Int", "SupaSimon21",
     "Kamen Rider Lim", "Caeruluna"])

# Make a function for each type of API request - (1) Summoner Request for basic info on user & (2) Match Request for
# user history & (3) Match Request for user game data

# API Request requirements:
# Summoner API: https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={api_key}
# user = chosenUsers[i]
key = api_key.KEY


def summoner_info(user, api_key):
    api_url = 'https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{user}?api_key={apikey}'
    request_url = api_url.format(user=user, apikey=api_key)
    request_call = requests.get(request_url).json()
    user_info = {"puuid": request_call['puuid'],
                 "accountId": request_call['accountId'],
                 "name": request_call['name']}

# User Match History API: https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{
# puuid}/ids?start=0&count=10&api_key={api_key}
# puuid = chosenUsers[i] puuid
# api_key = api_key.KEY

# Match Statisitcs API: https://americas.api.riotgames.com/lol/match/v5/matches/{matchid}?api_key={api_key}
# matchid = match ID from User's list
# api_key = api_key.KEY
