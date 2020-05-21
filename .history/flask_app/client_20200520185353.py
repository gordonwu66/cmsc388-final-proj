import requests

# Where the new python library/API should be implemented for use 

class PlayerBase(object):
    def __init__(self, player_json, flag, offense, defense, kicker):
        for i in flag:
            if i == 0:
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
                self.flags =['Base']
            if i == 1:
                self.flags.append('Offense')
                self.

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
        
        flag = [0]

        offense_url = player_url + f'/offense'
        resp = self.sess.get(offense_url)
        if resp.status_code == 200:
            flag.append(1)
            offense = []
            
            games_json = resp.json()['data']
            for game_json in games_json:
                offense.append(OffenseGame(game_json))

        defense_url = player_url + f'/defense'
        resp = self.sess.get(defense_url)
        if resp.status_code == 200:
            flag.append(2)
        defense = resp.json()
        
        kicker_url = player_url + f'/kickers'
        resp = self.sess.get(kicker_url)
        if resp.status_code == 200:
            flag.append(3)
        kicker = resp.json()
        
        player = PlayerBase(basic, flag, offense, defense, kicker)
        return player

    # def retrieve_movie_by_id(self, imdb_id):
    #     """ 
    #     Use to obtain a Movie object representing the movie identified by
    #     the supplied imdb_id
    #     """
    #     movie_url = self.base_url + f'i={imdb_id}&plot=full'

    #     resp = self.sess.get(movie_url)

    #     if resp.status_code != 200:
    #         raise ValueError('Search request failed; make sure your API key is correct and authorized')

    #     data = resp.json()

    #     if data['Response'] == 'False':
    #         print(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')
    #         return data

    #     movie = Movie(data, detailed=True)

    #     return movie

    # def search(self, search_string):
    #     """
    #     Searches the API for the supplied search_string, and returns
    #     a list of Media objects if the search was successful, or the error response
    #     if the search failed.

    #     Only use this method if the user is using the search bar on the website.
    #     """
    #     search_string = '+'.join(search_string.split())
    #     page = 1

    #     search_url = f's={search_string}&page={page}'

    #     resp = self.sess.get(self.base_url + search_url)
        
    #     if resp.status_code != 200:
    #         raise ValueError('Search request failed; make sure your API key is correct and authorized')

    #     data = resp.json()

    #     if data['Response'] == 'False':
    #         print(f'[ERROR]: Error retrieving results: \'{data["Error"]}\' ')
    #         return data 

    #     search_results_json = data['Search']
    #     remaining_results = int(data['totalResults'])

    #     result = []

    #     ## We may have more results than are first displayed
    #     while remaining_results != 0:
    #         for item_json in search_results_json:
    #             result.append(Movie(item_json))
    #             remaining_results -= len(search_results_json)
    #         page += 1
    #         search_url = f's={search_string}&page={page}'
    #         resp = self.sess.get(self.base_url + search_url)
    #         if resp.status_code != 200 or resp.json()['Response'] == 'False':
    #             break
    #         search_results_json = resp.json()['Search']

    #     return result


## -- Example usage -- ###
if __name__=='__main__':
    import os

    client = PlayerClient()

    players = client.all_players()

    for player in players:
        print(player.player_id)
    print(len(players))

    
