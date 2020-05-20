import requests

# Where the new python library/API should be implemented for use 

class PlayerBase(object):
    def __init__(self, player_json):
        self.player_id = player_json['player']
        self.fname = player_json['fname']
        self.lname = player_json['lname']
        self.pname = player_json['pname']
        self.pos1 = player_json['pos1']
        self.pos2 = player_json['pos2']
        self.height = player_json['height']
        self.weight = player_json['weight']
        self.dob = player_json['dob']
        self.dpos = player_json['dpos']
        self.col = player_json['col']
        self.dv = player_json['dv']
        self.start = player_json['start']
        self.cteam = player_json['cteam']
        self.posd = player_json['posd']
        self.jnum = player_json['jnum']
        self.dcp = player_json['dcp']

    def __repr__(self):
        return self.pname

class PlayerClient(object):
    
    def __init__(self):
        self.sess = requests.Session()
        self.base_url = f'https://www.armchairanalysis.com/api/1.0/test'

    def all_players(self):
        search_url = f'/players?status=active'
        resp = self.sess.get(self.base_url + search_url)

        if resp.status_code != 200:
            return ValueError('Unable to obtain all players, make sure url is correct')

        data = resp.json()

        all_players_json = data['data']

        result = []
        
        for item_json in all_players_json:
            result.append(PlayerBase(item_json))
        
        search_url = f'/players?status=active&start=1001'
        resp = self.sess.get(self.base_url + search_url)
        if resp.status_code != 200:
            return ValueError('Unable to obtain remaining players, make sure url is correct')
        data = resp.json()
        all_players_json = data['data']

        for item_json in all_players_json:
            result.append(PlayerBase(item_json))

        return result
    
    def retrieve_player_by_id(self, player_id):
        player_url = self.base_url + f'player/{player_id}'

        resp = self.sess.get(player_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper Player_Id given')

        data = resp.json()

        player = PlayerBase(data)

        return player


## -- Example usage -- ###
if __name__=='__main__':
    import os

    client = PlayerClient()


    players = client.all_players()

    for player in players:
        print(player)
    print(len(players))

    
