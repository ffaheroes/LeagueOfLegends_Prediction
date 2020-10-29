import json
import requests
from pymongo import MongoClient
import pandas as pd
import numpy as np
import time  # used for unixepochtime
from datetime import datetime  # used for unixepochtime
from sklearn.linear_model import LogisticRegression  # Machine Learning
from sklearn.datasets import load_iris
from sklearn.svm import LinearSVC
from sklearn.datasets import make_classification
import statistics
from statistics import mode
import random



mmrpoint = {'IRON IV': 0,
            'IRON III': 100,
            'IRON II': 200,
            'IRON I': 300,
            'BRONZE IV': 400,
            'BRONZE III': 500,
            'BRONZE II': 600,
            'BRONZE I': 700,
            'SILVER IV': 800,
            'SILVER III': 900,
            'SILVER II': 1000,
            'SILVER I': 1100,
            'GOLD IV': 1200,
            'GOLD III': 1300,
            'GOLD II': 1400,
            'GOLD I': 1500,
            'PLATINUM IV': 1600,
            'PLATINUM III': 1700,
            'PLATINUM II': 1800,
            'PLATINUM I': 1900,
            'DIAMOND IV': 1600,
            'DIAMOND III': 1700,
            'DIAMOND II': 1800,
            'DIAMOND I': 1900,
            }


champion_names = {
    1: 'Annie',
    2: 'Olaf',
    3: 'Galio',
    4: 'TwistedFate',
    5: 'XinZhao',
    6: 'Urgot',
    7: 'LeBlanc',
    8: 'Vladimir',
    9: 'Fiddlesticks',
    10: 'Kayle',
    11: 'Master Yi',
    12: 'Alistar',
    13: 'Ryze',
    14: 'Sion',
    15: 'Sivir',
    16: 'Soraka',
    17: 'Teemo',
    18: 'Tristana',
    19: 'Warwick',
    20: 'Nunu',
    21: 'MissFortune',
    22: 'Ashe',
    23: 'Tryndamere',
    24: 'Jax',
    25: 'Morgana',
    26: 'Zilean',
    27: 'Singed',
    28: 'Evelynn',
    29: 'Twitch',
    30: 'Karthus',
    31: "Cho'Gath",
    32: 'Amumu',
    33: 'Rammus',
    34: 'Anivia',
    35: 'Shaco',
    36: 'DrMundo',
    37: 'Sona',
    38: 'Kassadin',
    39: 'Irelia',
    40: 'Janna',
    41: 'Gangplank',
    42: 'Corki',
    43: 'Karma',
    44: 'Taric',
    45: 'Veigar',
    48: 'Trundle',
    50: 'Swain',
    51: 'Caitlyn',
    53: 'Blitzcrank',
    54: 'Malphite',
    55: 'Katarina',
    56: 'Nocturne',
    57: 'Maokai',
    58: 'Renekton',
    59: 'JarvanIV',
    60: 'Elise',
    61: 'Orianna',
    62: 'Wukong',
    63: 'Brand',
    64: 'LeeSin',
    67: 'Vayne',
    68: 'Rumble',
    69: 'Cassiopeia',
    72: 'Skarner',
    74: 'Heimerdinger',
    75: 'Nasus',
    76: 'Nidalee',
    77: 'Udyr',
    78: 'Poppy',
    79: 'Gragas',
    80: 'Pantheon',
    81: 'Ezreal',
    82: 'Mordekaiser',
    83: 'Yorick',
    84: 'Akali',
    85: 'Kennen',
    86: 'Garen',
    89: 'Leona',
    90: 'Malzahar',
    91: 'Talon',
    92: 'Riven',
    96: "Kog'Maw",
    98: 'Shen',
    99: 'Lux',
    101: 'Xerath',
    102: 'Shyvana',
    103: 'Ahri',
    104: 'Graves',
    105: 'Fizz',
    106: 'Volibear',
    107: 'Rengar',
    110: 'Varus',
    111: 'Nautilus',
    112: 'Viktor',
    113: 'Sejuani',
    114: 'Fiora',
    115: 'Ziggs',
    117: 'Lulu',
    119: 'Draven',
    120: 'Hecarim',
    121: "Kha'Zix",
    122: 'Darius',
    126: 'Jayce',
    127: 'Lissandra',
    131: 'Diana',
    133: 'Quinn',
    134: 'Syndra',
    136: 'AurelionSol',
    141: 'Kayn',
    142: 'Zoe',
    143: 'Zyra',
    145: "Kai'sa",
    150: 'Gnar',
    154: 'Zac',
    157: 'Yasuo',
    161: "Vel'Koz",
    163: 'Taliyah',
    164: 'Camille',
    201: 'Braum',
    202: 'Jhin',
    203: 'Kindred',
    222: 'Jinx',
    223: 'TahmKench',
    235: 'Senna',
    236: 'Lucian',
    238: 'Zed',
    240: 'Kled',
    245: 'Ekko',
    246: 'Qiyana',
    254: 'Vi',
    266: 'Aatrox',
    267: 'Nami',
    268: 'Azir',
    350: 'Yuumi',
    360: 'Samira',
    412: 'Thresh',
    420: 'Illaoi',
    421: "Rek'Sai",
    427: 'Ivern',
    429: 'Kalista',
    432: 'Bard',
    497: 'Rakan',
    498: 'Xayah',
    516: 'Ornn',
    517: 'Sylas',
    518: 'Neeko',
    523: 'Aphelios',
    555: 'Pyke',
    777: 'Yone,',
    875: 'Sett',
    876: 'lillia'

}

client = MongoClient('mongodb://localhost:27017/')

api_key = "Riotkey"

global History
History = {}

def apicall(apirequest,optarg=None):
    request = requests.get(apirequest)
    if request.status_code == 404:
        print("404")
        print(apirequest)
        print("trying again - Sleeping for 10sec")
        time.sleep(10)
        request = "404"
    elif request.status_code == 400:
        print("400")
        print(apirequest)
    elif request.status_code == 429:
        print("429 - excess - sleeping 60sec")
        time.sleep(60)
        request = requests.get(apirequest)
        if request.status_code == 429:
            print("429 - excess - sleeping 60sec")
            time.sleep(60)
            request = requests.get(apirequest)
        if request.status_code == 504:
            print("504 - Gateway timeout - retry")
            time.sleep(2)
            request = requests.get(apirequest)
    elif request.status_code == 503:
        print("503 - service unavailable, sleeping 2min")
        time.sleep(120)
        request = requests.get(apirequest)
    elif request.status_code == 500:
        print("500 - Internal server error, sleeping 2min")
        time.sleep(120)
        request = requests.get(apirequest)
    elif request.status_code == 504:
        print("504 - Gateway timeout - retry")
        time.sleep(2)
        request = requests.get(apirequest)
    else:
        print(apirequest)
        x = 2
    return request

def get_historic_soloQ(loop, server, player):
    # Getting the account id of the player
    apirequest ="https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format(server, player, api_key)
    print(player)
    print(apirequest)
    get_account_id = apicall(apirequest)
    accountId = json.loads(get_account_id.text)["accountId"]
    _id = json.loads(get_account_id.text)["id"]
    print(_id)
    endTime = int(time.time()) * 1000
    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Matches"]
    #collection.drop() #to activate if reset
    # Getting the matchlist
    apirequest = "https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?endIndex={}&beginIndex={}&api_key={}".format(server, accountId, loop, 0, api_key)
    matches_data= apicall(apirequest)
    matches = json.loads(matches_data.text)['matches']
    eta=0

    i = 1
    for match in matches:
        print(eta)


        queue = match["queue"]
        if match["queue"] != 420:
            continue

        apirequest = "https://{}.api.riotgames.com/lol/match/v4/matches/{}?&api_key={}".format(server, match['gameId'], api_key)
        game_data= apicall(apirequest)
        jsonwin = json.loads(game_data.text)

        side, result = get_side(jsonwin,accountId)
        role, dataquality = get_role(jsonwin,accountId,side,match["timestamp"])

        if dataquality == 0:
            print("Bad Data Quality -> Next game")
            continue

        print(role)
        match1 = {}
        match1["player"] = player
        match1["accountId"] = accountId
        match1["gameId"] = match['gameId']
        match1["result"] = result
        match1["timestamp"] = match["timestamp"]
        try :
            match1["Top"] = role["Top"]
            match1["Jungle"] = role["Jungle"]
            match1["Mid"] = role["Mid"]
            match1["ADC"] = role["ADC"]
            match1["Support"] = role["Support"]
            collection.insert_one(match1)
        except:
            print("Bad Data Quality -> Next game")
            continue

        eta+=1

    return accountId


def get_side(jsonwin, accountId):
    for i in range(10):
        try:
            if accountId == jsonwin['participantIdentities'][i]['player']['currentAccountId']:
                break  # break here
        except KeyError:
            print("keyerror")
            break  # break here.

    result = jsonwin['participants'][i]['stats']['win']
    side = jsonwin['participants'][i]['teamId']
    if side == 100:
        side = "blue"
    else:
        side = "red"

    return side, result

def get_role(jsonwin, accountId, side, timestamp):
    team1 = {}
    team2 = {}
    team1placeholder = {}
    team2placeholder = {}
    dataquality=1
    role_class = ['Top','Jungle','Mid','ADC','Support']
    duo = 0
    for i in range(10):
        role = jsonwin['participants'][i]['timeline']['role']
        lane = jsonwin['participants'][i]['timeline']['lane']
        currentAccountId = jsonwin['participantIdentities'][i]['player']['currentAccountId']
        champion = champion_names[jsonwin['participants'][i]['championId']]
        player = jsonwin['participantIdentities'][i]['player']['summonerName']
        summonerId = jsonwin['participantIdentities'][i]['player']['summonerId']
        accountId = jsonwin['participantIdentities'][i]['player']['accountId']
        if i == 5:
            duo = 0

        if role == "DUO_SUPPORT":
            role = "Support"
        elif role == "DUO_CARRY":
            role = "ADC"
        elif role == "SOLO" and lane == "TOP":
            role = "Top"
        elif role == "SOLO" and lane == "MIDDLE":
            role = "Mid"
        elif role == "NONE" and lane == "JUNGLE":
            role = "Jungle"
        elif role == "SOLO" and lane == "BOTTOM":
            role = "Support"


        if i<5:
            if role == "DUO":
                team1placeholder[i] = {'player': player, 'champion': champion, 'currentAccountId': currentAccountId, 'summonerId': summonerId, 'accountId':accountId}
            else:
                team1[role] = {'player': player, 'champion': champion, 'currentAccountId': currentAccountId, 'summonerId': summonerId, 'accountId':accountId}
        else:
            if role == "DUO":
                team2placeholder[i] = {'player': player, 'champion': champion, 'currentAccountId': currentAccountId,
                                       'summonerId': summonerId, 'accountId': accountId}
            else:
                team2[role] = {'player': player, 'champion': champion, 'currentAccountId': currentAccountId, 'summonerId': summonerId,'accountId':accountId}

    if team1placeholder:
        found = list(team1)
        c = [element for element in role_class if element not in found ]
        i=0
        for role in c:
            try:
                team1[role] = team1placeholder[list(team1placeholder.keys())[i]]
                i+=1
            except:
                dataquality = 0
                break

    if team2placeholder:
        found = list(team2)
        c = [element for element in role_class if element not in found ]
        i=0
        for role in c:
            try:
                team2[role] = team2placeholder[list(team2placeholder.keys())[i]]
                i+=1
            except:
                dataquality = 0
                break

    if set(team2.keys())!=set(team1.keys()): #checking if both team have identical role
        dataquality=0

    role ={}

    if side == "blue" and dataquality==1:
        for key in team1.keys():
            print(team1[key]['player'])
            history, totalgames = get_history(team1[key]['currentAccountId'], timestamp, team1[key]['accountId'])
            role[key] = {'player': team1[key]['player'],
                         'champ': team1[key]['champion'],
                         'matchup': team2[key]['champion'],
                         'currentAccountId': team1[key]['currentAccountId'],
                         'mmr': get_rank(team1[key]['summonerId']),
                         'masteries': get_mastery(team1[key]['summonerId']),
                         'history': history,
                         'totalgames': totalgames
                         }

    elif side == "red" and dataquality==1:
        for key in team2.keys():
            print(team2[key]['player'])
            history, totalgames = get_history(team2[key]['currentAccountId'], timestamp, team2[key]['accountId'])
            role[key] = {'player': team2[key]['player'],
                         'champ': team2[key]['champion'],
                         'matchup': team1[key]['champion'],
                         'currentAccountId': team2[key]['currentAccountId'],
                         'mmr': get_rank(team2[key]['summonerId']),
                         'masteries': get_mastery(team2[key]['summonerId']),
                         'history': history,
                         'totalgames': totalgames
                         }


    return role, dataquality



def get_rank(summonerid):
    apirequest = ("https://{}.api.riotgames.com/lol/league/v4/entries/by-summoner/{}?&api_key={}".format("euw1", summonerid, api_key))
    game_data = apicall(apirequest)
    mmr_score = 0
    if game_data.text == []:
        rating = "unranked"
        mmr_score = 1500
    else:
        dictio = (json.loads(game_data.text))
        for o in range(len(dictio)):
            if dictio[o]['queueType'] == "RANKED_SOLO_5x5":
                tier = dictio[o]['tier']
                rank = dictio[o]['rank']
                rankpoint = tier + " " + rank
                leaguePoints = dictio[o]['leaguePoints']
                mmr_score = mmrpoint[rankpoint] + leaguePoints
                rating = tier + " " + rank + " " + str(leaguePoints) + " LP"
                break

    return mmr_score


def get_mastery(summonerid):
    apirequest = ("https://{}.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/{}?&api_key={}".format("euw1", summonerid, api_key))
    mastery_data = apicall(apirequest)
    mastery = json.loads(mastery_data.text)
    l = 0
    Masteries = {}
    for champ in mastery:
        if l > 19:
            break
        Masteries[champion_names[champ['championId']]] = champ['championPoints']
        l += 1
    return Masteries

def get_history(currentAccountId,timestamp,accountId):
    endTime = timestamp - 2000 #33min before last game
    beginTime = timestamp - 604800 *1000 #Last week
    server = "euw1"
    apirequest = "https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}?endTime={}&beginTime={}&api_key={}".format(server, currentAccountId, endTime, beginTime, api_key)
    matches_data = apicall(apirequest)
    if matches_data == "404" :
        return "No games", 0 #return previous value of history watch out
    matches = json.loads(matches_data.text)['matches']
    totalgames = json.loads(matches_data.text)['totalGames']
    v=0
    History = {}
    for match in matches:
        if v > 4:
            break
        server = match['platformId']
        apirequest = "https://{}.api.riotgames.com/lol/match/v4/matches/{}?&api_key={}".format(server, match['gameId'], api_key)
        game_data = apicall(apirequest)
        jsonwin = json.loads(game_data.text)
        for i in range(10):
            try:
                if accountId == jsonwin['participantIdentities'][i]['player']['currentAccountId']:
                    i += 1
                    break    # break here
            except KeyError:
                print(accountId)
                print("keyerror")
                print(i)
                i += 1
                break    # break here


        if jsonwin['participants'][i - 1]['stats']['win'] == True:
            result = "Win"
        else:
            result = "Loss"

        if jsonwin['participants'][i - 1]['stats']['deaths'] ==0 :
            death = 1
        else:
            death = jsonwin['participants'][i - 1]['stats']['deaths']




        role = match['role']
        lane = match['lane']

        if role == "DUO_SUPPORT":
            role="Support"
        elif role == "DUO_CARRY":
            role="ADC"
        elif role == "SOLO" and lane =="TOP":
            role="Top"
        elif role == "SOLO" and lane == "MIDDLE":
            role = "Mid"
        elif role == "NONE" and lane == "JUNGLE":
            role = "Jungle"

        History[str(v)] = { 'gameId' : match['gameId'], 'result' : result , 'role' : role, 'champion' : champion_names[match['champion']] , 'KDA' :  str(jsonwin['participants'][i - 1]['stats']['kills']) + "/" + str(jsonwin['participants'][i - 1]['stats']['deaths']) + "/" + str(jsonwin['participants'][i - 1]['stats']['assists']) , 'KDA2' :  (jsonwin['participants'][i - 1]['stats']['kills'] + jsonwin['participants'][i - 1]['stats']['assists'] )/ death }

        v = v + 1
    return History, totalgames


def winorlose(result):
    if result == "Win":
        winorlose = "Win"
    else:
        winorlose = "Loss"
    return winorlose


def tilt_score(first, second, third, fourth, fifth):
    weight = np.array([40, 25, 17.5, 10, 7.5])
    if first is None:
        first = "Loss"
    if second is None:
        second = "Loss"
    if third is None:
        third = "Loss"
    if fourth is None:
        fourth = "Loss"
    if fifth is None:
        fifth = "Loss"
    result = [first, second, third, fourth, fifth]
    result = ['None' if v is None else v for v in result]
    print(result)
    result = [str2bool(first),str2bool(second),str2bool(third),str2bool(fourth),str2bool(fifth)]
    # print(result)
    opposite_result = [not i for i in result]
    tilt = (weight * opposite_result)
    tilt_score = np.sum(tilt)

    return tilt_score

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1", "win")


def update_model():
    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Matches"]
    cursor = collection.find({}, no_cursor_timeout=True).batch_size(200)
    for document in cursor:
        dbmongo = client["MetAnalyser"]
        collection = dbmongo["Teammate"]
        gameId = document["gameId"]
        cursor = collection.find({'gameIdref': gameId})
        panda = pd.DataFrame(list(cursor))
        if len(panda.index) < 1:
            break
        try:
            teammates_accountId = [document['teammate1']['summonerId'], document['teammate2']['summonerId'], document['teammate3']['summonerId'], document['teammate4']['summonerId']]
        except:
            break
    # print(teammates_accountId)
        print(document["gameId"])
        summoner = []

        for j in teammates_accountId:
            teammate = panda.loc[panda['summonerId'] == j]
            first10 = teammate.head(10)
            if len(first10.index) >= 5:
                streak = winorlose(first10.iloc[0, 6]) + " " + winorlose(first10.iloc[1, 6]) + " " + winorlose(first10.iloc[2, 6]) + " " + winorlose(first10.iloc[3, 6]) + " " + winorlose(first10.iloc[4, 6])
                tilt = tilt_score(first10.iloc[0, 6], first10.iloc[1, 6], first10.iloc[2, 6], first10.iloc[3, 6], first10.iloc[4, 6])
            else:
                i = 0
                streak = ""
                tilt = 0
                while i < len(first10.index):
                    streak = streak + " " + winorlose(first10.iloc[i, 6])
                    weight = np.array([40, 25, 17.5, 10, 7.5])
                    result = not first10.iloc[i, 6]
                    tilt = tilt + result * weight[i]
                    i += 1
            streak = streak.lstrip()

            # --------------------------Getting MMR ---------------------------------------------------------------------------------
            apirequest = ("https://{}.api.riotgames.com//lol/league/v4/entries/by-summoner/{}?&api_key={}".format("euw1", j, api_key))
            game_data = apicall(apirequest)
            if game_data.text == []:
                rating = "unranked"
                mmr = 1500
            else:
                dictio = (json.loads(game_data.text))
                # print(len(dictio))
                for i in range(len(dictio)):
                    if dictio[i]['queueType'] == "RANKED_SOLO_5x5":
                        tier = dictio[i]['tier']
                        rank = dictio[i]['rank']
                        rankpoint = tier + " " + rank
                        leaguePoints = dictio[i]['leaguePoints']
                        mmr = mmrpoint[rankpoint] + leaguePoints
                        # print(mmr)
                        rating = tier + " " + rank + " " + str(leaguePoints) + " LP"
                        break

            # --------------------------Getting Masteries ---------------------------------------------------------------------------------

            apirequest = ("https://{}.api.riotgames.com//lol/champion-mastery/v4/champion-masteries/by-summoner/{}?&api_key={}".format("euw1", j, api_key))
            # print("https://{}.api.riotgames.com//lol/champion-mastery/v4/champion-masteries/by-summoner/{}?&api_key={}".format("euw1", j, api_key))
            mastery_data = apicall(apirequest)
            mastery = json.loads(mastery_data.text)

            i = 0
            Masteries = {}
            for champ in mastery:
                if i > 19:
                    break

                # x = {champion_names[champ['championId']]: champ['championPoints']}
                # Masteries.append(x)
                Masteries[champion_names[champ['championId']]] = champ['championPoints']
                i += 1
            # print(champion_names[champ['championId']] + " " + str(champ['championPoints']))

            # --------------------------Winrate ---------------------------------------------------------------------------------

            x = teammate["result"].agg(['sum', 'size'])
            win = round(x.iloc[0] / x.iloc[1], 3) * 100
            playerinfo = [{"accounId": j, "streak": streak, "rank": mmr, "winrate": win, "tilt": tilt, "champions": Masteries}]
            summoner.extend(playerinfo)

            dbmongo = client["MetAnalyser"]
            collection = dbmongo["Matches"]
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"model": summoner}}
            collection.update_many(myquery, newvalues)
        # print(summoner)
    return summoner


def update_model_masteryscore():
    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Matches"]
    cursor = collection.find()
    df1 = pd.DataFrame(collection.find())
    df1 = df1[['gameId','teammate1','teammate2','teammate3','teammate4','model']]
    for index, row in df1.iterrows():
        masteryscore =0
        # print(row['gameId'])
        for i in range(4):
            if row['teammate'+str(i+1)]['summonerId'] == row['model'][i]['accounId']:
                adict = row['model'][i]['champions']
            # print(adict)
                try:
                    if adict[row['teammate'+str(i+1)]['champion']] >200000:
                        masteryscore += 150
                    elif adict[row['teammate'+str(i+1)]['champion']] >100000:
                        masteryscore += 90
                    elif adict[row['teammate'+str(i+1)]['champion']] >50000:
                        masteryscore += 50
                    elif adict[row['teammate'+str(i+1)]['champion']] >25000:
                        masteryscore += 25
                    elif adict[row['teammate'+str(i+1)]['champion']] <25000:
                        masteryscore += -10
                except KeyError:

                # print("not present")
                    masteryscore+=-20
                # Key is not present
                pass
        # print(masteryscore)
        dbmongo = client["MetAnalyser"]
        collection = dbmongo["Matches"]
        myquery = {"gameId": row['gameId']}
        newvalues = {"$set": {"MasteryScore": masteryscore}}
        collection.update_many(myquery, newvalues)
    return

def update_model_tiltscore_winrate():

    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Matches"]
    cursor = collection.find()

    for document in cursor:
        gameId = document["gameId"]
        result = document["result"]
        df = pd.DataFrame(document["model"])
        tilt = df.mean(axis=0)[1]
        win = df.mean(axis=0)[2]
        if tilt < 60 and win > 45 and document["MasteryScore"] >-100 :
        # print("play it")
            dbmongo = client["MetAnalyser"]
            collection = dbmongo["Matches"]
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"play_it": True}}
            collection.update_many(myquery, newvalues)
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"winrate": win}}
            collection.update_many(myquery, newvalues)
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"tiltscore": tilt}}
            collection.update_many(myquery, newvalues)
        else:
        # print("Dodge")
            dbmongo = client["MetAnalyser"]
            collection = dbmongo["Matches"]
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"play_it": False}}
            collection.update_many(myquery, newvalues)
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"winrate": win}}
            collection.update_many(myquery, newvalues)
            myquery = {"gameId": document["gameId"]}
            newvalues = {"$set": {"tiltscore": tilt}}
            collection.update_many(myquery, newvalues)
    return


def get_summonerId(player):
        apirequest = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format("euw1", player, key)
        print(apirequest)
        api_data = apicall(apirequest)
        accountId = json.loads(api_data.text)["accountId"]
        summonId = json.loads(api_data.text)["id"]
        return summonId

def get_currentAccountId(player):
        apirequest = "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}?api_key={}".format("euw1", player, key)
        api_data = apicall(apirequest)
        currentAccountId = json.loads(api_data.text)["accountId"]
        summonId = json.loads(api_data.text)["id"]
        return currentAccountId


def playerinfo(player):
    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Teammate_oneoff"]
    summonerId = get_summonerId(player)
    mmr = get_rank(summonerId)
    Masteries = get_mastery(summonerId)
    currentAccountId = get_currentAccountId(player)
    History = get_history(currentAccountId,int(time.time()) * 1000)
    tilt = tilt_score(History.get(str(0), {}).get('result'),History.get(str(1), {}).get('result'),History.get(str(2), {}).get('result'),History.get(str(3), {}).get('result'),History.get(str(4), {}).get('result'))
    streak =  winorlose(History.get(str(0), {}).get('result')) + " " + winorlose(History.get(str(1), {}).get('result')) + " " + winorlose(History.get(str(2), {}).get('result')) + " " + winorlose(History.get(str(3), {}).get('result')) + " " + winorlose(History.get(str(4), {}).get('result'))

    data = pd.DataFrame.from_dict(History).T
    print(data)
    mostcommonlane = data['lane'].value_counts().idxmax()
    mostcommonchamp = data['champion'].value_counts().idxmax()
    averagekda = data["KDA2"].mean()
    mostcommonchamp = data['champion'].value_counts().idxmax()
    winrate = len(data[data['result'] == "Win"]) / ( len(data[data['result'] == "Win"]) + len(data[data['result'] == "Loss"]) )
    print(player)
    print(winrate)


    match1 = {}
    match1["player"] = player
    match1["accountId"] = currentAccountId
    match1["winrate"] = winrate
    match1["tiltscore"] = tilt
    match1["streak"] = streak
    match1["info"] = {"summonerId": summonerId, "accountId": currentAccountId, "summonerName": player, 'tiltscore': tilt, 'streak' : streak, "mmr" : mmr , "lane" : mostcommonlane, "KDA": averagekda, "champion": mostcommonchamp, "top20champ": Masteries , "History" : History }

    collection.insert_one(match1)


def getrandomplayer():
    role = ['Top','ADC','Mid','Jungle','Support']
    dbmongo = client["MetAnalyser"]
    collection = dbmongo["Matches"]
    cursor = collection.find()
    count = collection.count()
    last = collection.find().sort([("_id",-1)]).limit(1)
    for document in last:
        print(document["gameId"])
        num1 = random.randint(0, 4)
        choose = role[num1]
        player = document[choose]["player"]
    return player


dbmongo = client["MetAnalyser"]
collection = dbmongo["Matches"]


for i in range(30):
    summoner = getrandomplayer()
    print(summoner)
    print(i)
    get_historic_soloQ(20, "euw1", summoner)
