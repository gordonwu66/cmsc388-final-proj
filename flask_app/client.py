import requests

# Where the new python library/API should be implemented for use 

class PlayerBase(object):
    def __init__(self, player_json, offense=[], defense=[], kicker=[], flags=[]):
        self.player_id = player_json['player']
        self.fname = player_json['fname']
        self.lname = player_json['lname']
        self.pname = player_json['pname']
        self.fullname = self.fname + " " + self.lname
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
        self.offense = offense
        self.defense = defense
        self.kicker = kicker
        self.flags = flags

    def __repr__(self):
        return self.fullname

class OffenseGame(object):
    def __init__(self, game_json):
        self.player_id = game_json['player']
        self.gid = game_json['gid']
        self.pa = game_json['pa']
        self.pc = game_json['pc']
        self.py = game_json['py']
        self.ints = game_json['ints']
        self.tdp = game_json['tdp']
        self.ra = game_json['ra']
        self.sra = game_json['sra']
        self.ry = game_json['ry']
        self.tdr = game_json['tdr']
        self.trg = game_json['trg']
        self.rec = game_json['rec']
        self.recy = game_json['recy']
        self.tdrec = game_json['tdrec']
        self.ret = game_json['ret']
        self.rety = game_json['rety']
        self.tdret = game_json['tdret']
        self.fuml = game_json['fuml']
        self.peny = game_json['peny']
        self.snp = game_json['snp']
        self.fp = game_json['fp']
        self.fp2 = game_json['fp2']
        self.fp3 = game_json['fp3']
        self.game = game_json['game']
        self.seas = game_json['seas']
        self.year = game_json['year']
        self.team = game_json['team']
    
    def __repr__(self):
        return self.gid

class DefenseGame(object):
    def __init__(self, game_json):
        self.player_id = game_json['player']
        self.gid = game_json['gid']
        self.solo = game_json['solo']
        self.comb = game_json['comb']
        self.sck = game_json['sck']
        self.saf = game_json['saf']
        self.blk = game_json['blk']
        self.ints = game_json['ints']
        self.pdef = game_json['pdef']
        self.frcv = game_json['frcv']
        self.forc = game_json['forc']
        self.tdd = game_json['tdd']
        self.rety = game_json['rety']
        self.tdret = game_json['tdret']
        self.peny = game_json['peny']
        self.snp = game_json['snp']
        self.fp = game_json['fp']
        self.fp2 = game_json['fp2']
        self.game = game_json['game']
        self.seas = game_json['seas']
        self.year = game_json['year']
        self.team = game_json['team']
    
    def __repr__(self):
        return self.gid

class KickerGame(object):
    def __init__(self, game_json):
        self.player_id = game_json['player']
        self.gid = game_json['gid']
        self.pat = game_json['pat']
        self.fgs = game_json['fgs']
        self.fgm = game_json['fgm']
        self.fgl = game_json['fgl']
        self.fp = game_json['fp']
        self.game = game_json['game']
        self.seas = game_json['seas']
        self.year = game_json['year']
        self.team = game_json['team']
    
    def __repr__(self):
        return self.gid

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

        return result

    def get_players_by_team(self, tname):
        print(tname)
        player_url = self.base_url + f'/players/{tname}'

        resp = self.sess.get(player_url)

        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper team name given')

        data = resp.json()

        all_players_json = data['data']

        result = []
        
        for item_json in all_players_json:
            result.append(PlayerBase(item_json))

        return result

    def retrieve_player_by_id(self, player_id):
        player_url = self.base_url + f'/player/{player_id}'

        resp = self.sess.get(player_url)
        
        if resp.status_code != 200:
            raise ValueError('Search request failed, make sure proper Player_Id given')
        data = resp.json()
        basic = data['data']

        flag = []
        offense = []
        defense = []
        kicker = []

        offense_url = player_url + f'/offense'
        resp = self.sess.get(offense_url)
        if resp.status_code == 200:
            flag.append(1)
            games_json = resp.json()['data']
            for game_json in games_json:
                offense.append(OffenseGame(game_json))

        defense_url = player_url + f'/defense'
        resp = self.sess.get(defense_url)
        if resp.status_code == 200:
            flag.append(2)
            games_json = resp.json()['data']
            for game_json in games_json:
                defense.append(DefenseGame(game_json))
        
        kicker_url = player_url + f'/kickers'
        resp = self.sess.get(kicker_url)
        if resp.status_code == 200:            
            flag.append(3)
            games_json = resp.json()['data']
            for game_json in games_json:
                kicker.append(KickerGame(game_json))
        
        player = PlayerBase(basic, offense=offense, defense=defense, kicker=kicker, flags=flag)
        return player

    def retrieve_player_by_name(self, player_fname, player_lname):
        player_url = self.base_url + f'/player/{player_fname}_{player_lname}'
        print(player_fname + player_lname)
        resp = self.sess.get(player_url)
        
        if resp.status_code != 200:
            #raise ValueError('Search request failed, make sure proper Player Name given')
            return resp.json()
        data = resp.json()
        basic = data['data'][0]
        return basic['player']

## -- Example usage -- ###
if __name__=='__main__':
    import os

    client = PlayerClient()

    players = client.all_players()

    for player in players:
        print(player.player_id)
    print(len(players))