from riotwatcher import LolWatcher, ApiError
import pyspark
from shared.credentials import key


#global variables
watcher = LolWatcher(key)
my_region = 'LA1'

#rank multiplier to sort list
rank_multiplier =[
    {
        'CHALLENGER': 9000,
        'GRANDMASTER': 8000,
        'MASTER': 7000,
        'DIAMOND': 6000,
        'PLATINUM': 5000,
        'GOLD': 4000,
        'SILVER': 3000,
        'BRONZE': 2000,
        'IRON': 1000
    },
    {
        'IV' : 100,
        'III' : 300,
        'II' : 500,
        'I' : 700,
    }
]
#players lists
players = [
    'AK7 Dianel',
    'AK7 Nero',
    'AK7 Stevo',
    'AK7 Secuela',
    'AK7 LuisFock',
    'AK7 CARLOSFV',
    'AK7 Mel',
    'Thayron',
    'AK7 Joel'
]
#Creating player object
class Player:
    def __init__(self, name):
        self.name = name
        self.elo = None
        self.rank = None
        self.tier = None
        self.points = None
    #function to calculate elo number
    def calculate_elo(self):
        get_id = watcher.summoner.by_name(my_region, self.name)
        get_ranked = watcher.league.by_summoner(my_region, get_id['id'])
        #find which dictionary has the soloqueue info
        for dictionary in get_ranked:
            if 'RANKED_SOLO_5x5' in dictionary.values():
                self.tier = dictionary['tier']
                self.rank = dictionary['rank']
                self.points = dictionary['leaguePoints']
                self.elo = rank_multiplier[0].get(self.tier, 0) + rank_multiplier[1].get(self.rank, 0) + self.points

    def __str__(self):
        return f"{self.name} -: {self.tier} {self.rank} {self.points}"

#empty list
player_objects = []
#loop to go through all players summoner name and calculate elo
for player_name in players:
    player = Player(player_name)
    player.calculate_elo()
    player_objects.append(player)
#sorting list from higher ranked on
sorted_players = sorted(player_objects, key=lambda p: p.elo, reverse=True)

for player in sorted_players:
    print(player)

#df_columns = ["Summoner Name","Rank","Division","Points"]
#df = 