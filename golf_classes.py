# golf_classes.py

class Player:
    def __init__(self, name):
        self.name = name
        self.rounds = []  # List of PlayerRoundInfo objects

class PlayerRoundInfo:
    def __init__(self, player, tournament_name, round_number, handicap, tee, hole_scores, total, net):
        self.player = player
        self.tournament_name = tournament_name
        self.round_number = round_number
        self.handicap = handicap
        self.tee = tee
        self.hole_scores = hole_scores  # List of 18 scores
        self.total = total
        self.net = net

class Tournament:
    def __init__(self, name):
        self.name = name
        self.rounds = []  # List of Round objects

class Round:
    def __init__(self, tournament_name, round_number):
        self.tournament_name = tournament_name
        self.round_number = round_number
        self.player_rounds = []  # List of PlayerRoundInfo objects

class Team:
    def __init__(self, name, members):
        self.name = name
        self.members = members  # List of Player objects
        self.aggregate_score = None