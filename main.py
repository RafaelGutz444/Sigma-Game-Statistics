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
# print(type(summoner_puuid), summoner_puuid, " puuid")

# API: Match-v5 --------------------------------------------------------------------------------------------------------
# Goal: Pull RAFIYO match history --------------------------------------------------------------------------------------

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

# CSV MatchHistory File Creation
fields = ['MatchID']
filename = 'MatchHistory.csv'
# print(match_request)

with open(filename, 'w') as csvFile:
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(fields)

    # Iterate through array to make each item from the array, a new row in csv
    i = 0
    for i in match_request:
        csvWriter.writerow([i])

# API: Match-v5 --------------------------------------------------------------------------------------------------------
# Goal: Iterate through every MatchID in MatchHistory.csv and pull specific match team summary data --------------------

# Can reuse url parameters from last section because we're calling from the same API
match_summary_parameter = ''
match_summary_ids = '?'
match_summary_path_parameter = []
# A separate API request for each MatchID we need data from.
with open(filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    columnHeader = next(csv_reader)
    for row in csv_reader:
        match_summary_path_parameter.append(row)

    # k = 0
    # for k in range(0, len(match_summary_path_parameter)):
    #     match_info_call = API_URL.format(region=match_region, api_name=match_apiName, version=match_version,
    #                                      api_name_plural=match_name_plural, parameter=match_summary_parameter,
    #                                      path_parameter=match_summary_path_parameter[], match_ids=match_summary_ids,
    #                                      api_key=app_key)
    #     match_info = requests.get(match_info_call).json()
    #     k += 1
    API_URL1 = "https://{region}.api.riotgames.com/lol/{api_name}/{version}/{api_name_plural}/{" \
               "path_parameter}{match_ids}api_key={api_key}"

    match_info_call = API_URL1.format(region=match_region, api_name=match_apiName, version=match_version,
                                      api_name_plural=match_name_plural, parameter=match_summary_parameter,
                                      path_parameter=match_summary_path_parameter[0][0], match_ids=match_summary_ids,
                                      api_key=app_key)

    match_info = requests.get(match_info_call).json()
    print(match_info['metadata']['participants'])

with open('MatchSummary.csv', 'w') as matchSummary:
    fields = ['Participants']
    writer = csv.DictWriter(matchSummary, fieldnames=fields)
    writer.writeheader()