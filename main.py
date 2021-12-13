import api_key
import requests
import csv

API_URL = "https://{region}.api.riotgames.com/lol/{api_name}/{version}/{api_name_plural}/by-{parameter}/{" \
          "path_parameter}{match_ids}api_key={api_key}"

app_key = api_key.KEY  # API key call

# API: Summoner-v4
# Goal: Pull puuid to utilize in other requests to get match data
summoner_region = "na1"
summoner_apiName = "summoner"
summoner_version = "v4"
summoner_name_plural = "summoners"
summoner_parameter = "name"
summoner_path_param = "RAFIYO?"
summoner_match_ids = ""
# summoner_call builds up the url we're using to request to get summoner puuid
summoner_call = API_URL.format(region=summoner_region, api_name=summoner_apiName, version=summoner_version,
                               api_name_plural=summoner_name_plural, parameter=summoner_parameter,
                               path_parameter=summoner_path_param, match_ids=summoner_match_ids, api_key=app_key)

summoner_request = requests.get(summoner_call).json()  # The actual API request using the link we built above.
# ".json()" method converts the string response into a python dictionary type so we may call the specific info we need.

summoner_puuid = summoner_request['puuid']  # calls for the puuid from the API response
print(type(summoner_puuid), summoner_puuid, " puuid")

# API: Match-v5
# Goal: Pull RAFIYO match history

match_region = "americas"
match_apiName = "match"
match_version = "v5"
match_name_plural = "matches"
match_parameter = "puuid"
match_path_parameter = summoner_puuid
match_ids = "/ids?start=0&count=50&"

match_call = API_URL.format(region=match_region, api_name=match_apiName, version=match_version,
                            api_name_plural=match_name_plural, parameter=match_parameter,
                            path_parameter=match_path_parameter, match_ids=match_ids, api_key=app_key)

match_request = requests.get(match_call).json()
match_history = match_request
i = 0
i: int
for i in range(0, len(match_history)):
    print(match_history[i], '\n')
    i += 1
