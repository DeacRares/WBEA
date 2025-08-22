import json

class WeaponBall:
    def __init__(self,name):
        self.name = name
        self.elo = 1000
        self.wins = 0
        self.loses = 0
        self.placement = -1

    def display(self):
        print(f'{self.name} - elo : {self.elo} - record : {self.wins}-{self.loses}')
    
    def update_info(self):
        pass

info_path = 'info.json'
weaponballs = {}
data = {}
final_list = []
info_dict ={}

def update_info():
    old_info = {}
    with open('info.json', 'r') as file:
        old_info = json.load(file)
    reversed_list = final_list[::-1]
    for val in reversed_list:
        info_dict[val.name]={
            'elo' : val.elo,
            'wins' : val.wins,
            'loses' : val.loses,
            'placement': val.placement,}
        try:
            info_dict[val.name]['change'] = old_info[val.name]['placement']-val.placement
        except KeyError:
            info_dict[val.name]['change'] =0

            

    same = True
    for key, value in info_dict.items():
        for k, val in value.items():
            if k!='change':
                if val !=old_info[key][k]:
                    same = False
    if not same:
        with open(info_path, 'w') as file:
            json.dump(info_dict, file, indent = 4)
    else:
        print('no change')


def elo_change(winner_rating, loser_rating, k=64):
    expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
    change = k * (1 - expected_winner)
    return int(round(change))


def init_competitors():
    for value in data.values():
        for key,ball in value.items():
            if key not in ['format', 'score']:
                if ball not in weaponballs:
                    weaponballs[ball] = WeaponBall(ball)

def elo_determination():
    for value in data.values():
        change = elo_change(weaponballs[value['winner']].elo,weaponballs[value['loser']].elo)
        weaponballs[value['winner']].elo +=change
        weaponballs[value['winner']].wins += 1
        weaponballs[value['loser']].elo =max(weaponballs[value['loser']].elo-change, 100)
        weaponballs[value['loser']].loses += 1

def sort_the_list():
    lst = []
    for value in weaponballs.values():
        lst.append(value)
    lst.sort(key=lambda x: x.elo)
    return lst

if __name__=='__main__':

    with open('data.json', 'r') as file:
        data = json.load(file)

    init_competitors()
    elo_determination()
    final_list = sort_the_list()
    update_info()

