
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
match_ids = "/ids?start=0&count=1&" # 10 or higher violates API request limits

match_call = API_URL.format(region=match_region, api_name=match_apiName, version=match_version,
                            api_name_plural=match_name_plural, parameter=match_parameter,
                            path_parameter=match_path_parameter, match_ids=match_ids, api_key=app_key)

match_request = requests.get(match_call).json()  # ------------------- MATCHID USED TO GET USERS ----------------------
participant_list = []
# CSV MatchHistory File Creation
fields = ['MatchID']
filename = 'MatchHistory.csv'

with open(filename, 'w') as csvFile:
    csvWriter = csv.writer(csvFile)

    # Iterate through array to make each item from the array, a new row in csv
    i = 0
    for i in match_request:
        csvWriter.writerow([i])

# API: Match-v5 --------------------------------------------------------------------------------------------------------
# Goal: Iterate through every MatchID in MatchHistory.csv --------------------------------------------------------------

# Can reuse url parameters from last section because we're calling from the same API
match_summary_parameter = ''
match_summary_ids = '?'
match_summary_path_parameter = []

with open(filename, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    columnHeader = next(csv_reader)
    for row in csv_reader:
        match_summary_path_parameter.append(row)
        # print(row)
    # print(match_summary_path_parameter)

# API: MAtch-v5 --------------------------------------------------------------------------------------------------------
# Goal: Iterate Match History to pull all puuids (basically user IDs).
def summonerNames():
    API_URL1 = "https://{region}.api.riotgames.com/lol/{api_name}/{version}/{api_name_plural}/{" \
               "path_parameter}{match_ids}api_key={api_key}"
    summonerList = []
    g = 0
    while g in range(0, len(match_summary_path_parameter)):

        match_info_call = API_URL1.format(region=match_region, api_name=match_apiName, version=match_version,
                                      api_name_plural=match_name_plural, parameter=match_summary_parameter,
                                      path_parameter=match_summary_path_parameter[g][0], match_ids=match_summary_ids,
                                      api_key=app_key)
        match_info = requests.get(match_info_call).json()
        g += 1
        h = 0
        for h in range(0, len(match_info['info']['participants'])):
            summonerList.append(match_info['info']['participants'][h]['summonerName'])
        print(len(summonerList))

    summonerList = list(set(summonerList))
    print(len(summonerList), summonerList)
    return(summonerList)

summonerList = summonerNames() # List of all summoner names

chosenUsers = list(
    ["RAFIYO", "BraDeLeOh", "HydraSniper", "EddyDev", "M1dus", "KimJxngUn", "Young Int", "SupaSimon21",
     "Kamen Rider Lim", "Caeruluna"])

def summonerBio(chosenUsers):
    API_URL = "https://{region}.api.riotgames.com/lol/{api_name}/{version}/{api_name_plural}/by-{parameter}/{" \
              "path_parameter}{match_ids}?api_key={api_key}"
    summoner_region = "na1"
    summoner_apiName = "summoner"
    summoner_version = "v4"
    summoner_name_plural = "summoners"
    summoner_parameter = "name"
    summoner_path_param = chosenUsers
    summoner_match_ids = ""

    b = 0
    with open('SummonerList.csv', 'w') as csvfile:

        fields = ['puuid', 'accountId', 'name', 'summonerLevel']
        writer = csv.writer(csvfile)
        writer.writerow(fields)

        while b in range(0, len(chosenUsers)):
            summoner_call = API_URL.format(region=summoner_region, api_name=summoner_apiName, version=summoner_version,
                                       api_name_plural=summoner_name_plural, parameter=summoner_parameter,
                                       path_parameter=str(summoner_path_param[b]), match_ids=summoner_match_ids,
                                       api_key=app_key)
            summonerBio_call = requests.get(summoner_call).json()
            print(summoner_call)
            summonerStatHolder = [0, 0, 0, 0] # [0] = puuid | [1] = accountId | [2] = name | [3] = summonerLevel |
            print(summonerBio_call.keys())
            summonerStatHolder[0] = summonerBio_call['puuid']
            summonerStatHolder[1] = summonerBio_call['accountId']
            summonerStatHolder[2] = summonerBio_call['name']
            summonerStatHolder[3] = summonerBio_call['summonerLevel']
            b += 1
            z = 0
            writer.writerow(summonerStatHolder)  # Writes in values for puuid, accountId, name, summonerLevel attributes
    csvfile.close()

    # Only the fields row and the column of MatchIds are filled in. So now let's fill in the remaining rows.
    userStepper = 0
    # Let's start by reading the user CSV file to get the MatchID

    with open(chosenUsers[0]+'.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)


peopleBio = summonerBio(chosenUsers)

