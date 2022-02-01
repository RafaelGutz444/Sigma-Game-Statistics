import api_key
import requests
import csv

app_key = api_key.KEY  # API key call

API_URL = "https://{region}.api.riotgames.com/lol/{api_name}/{version}/{api_name_plural}/by-{parameter}/{" \
          "path_parameter}{match_ids}api_key={api_key}"

fields = []
rows = []

with open('SummonerList.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile)

    fields = next(csvreader)  # Capture fields

    for row in csvreader:
        rows.append(row)
#

# print(rows[0][0])  # [#1 index] calls the specific row / summoner [#2 index] calls the item within that row.
# [0] = puuid [1] = accountId [2] = name [3] = summonerlevel

for i in range(0, len(rows)):
    summonerPuuid = rows[i][0]

    match_region = "americas"
    match_apiName = "match"
    match_version = "v5"
    match_name_plural = "matches"
    match_parameter = "puuid"
    match_ids = "/ids?start=0&count=10&"  # 10 or higher violates API request limits
    match_path_parameter = summonerPuuid

    match_call = API_URL.format(region=match_region, api_name=match_apiName, version=match_version,
                                api_name_plural=match_name_plural, parameter=match_parameter,
                                path_parameter=match_path_parameter, match_ids=match_ids, api_key=app_key)

    match_request = requests.get(match_call).json()  # ------------------- gets matchId history of specific user

    with open('{}.csv'.format(rows[i][2]), 'w') as csvfile:
        writeObject = csv.writer(csvfile)
        fields = ['MatchId', 'killCount', 'gold', 'damageDealt', 'wards', 'damageTaken', 'CS']
        writeObject.writerow(fields)

        for row in match_request:
            writeObject.writerow([row])

chosenUsers = list(
    ["RAFIYO", "BraDeLeOh", "HydraSniper", "EddyDev", "M1dus", "KimJxngUn", "Young Int", "SupaSimon21",
     "Kamen Rider Lim", "Caeruluna"])


# We need to read/collect the MatchIDs from each summoner.
# (1) First I'll open each summoner file individually.

def user_matchid_hold(chosen_users):
    h = 0

    matchesIDs = []
    if h <= len(chosenUsers):
        with open("{}.csv".format(chosenUsers[h]), 'r') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)
            for element in csv_reader:
                matchesIDs.append(element)
        h += 1
    return matchesIDs


match_ids = user_matchid_hold(chosenUsers)
print(match_ids)

# h = 0
# if h <= len(chosenUsers):
#     matchesIds = user_matchID_hold(chosenUsers)

# (2) Then, I'll write those MatchIDs onto an array.
# (3) Next, I'll make an API request for each MatchID
# (4) Then, I'll pull the specific info from each MatchID call.
# LOOP (through summoner files)
# LOOP (through MatchIDs in the summoner file)
