# golf_classes.py

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass


class Player:
    def __init__(self, name, sand_bag_factor=None):
        self.name = name
        self.rounds = []  # List of PlayerRoundInfo
        self.sand_bag_factor = sand_bag_factor

    def compute_sand_bag_factor(self, min_rounds=5, scale_factor=0.5):
        """
        Compute sand_bag_factor for the Player.
        If the number of tournament or casual rounds is below min_rounds,
        scale the result by scale_factor.
        """
        tournament_scores = [r.net for r in self.rounds if r.tournament_flag and r.net is not None]
        casual_scores = [r.net for r in self.rounds if not r.tournament_flag and r.net is not None]
        #print(f'player: {self.name}, tourments : {len(tournament_scores)}, casual_scores : {len(casual_scores)}')

        if tournament_scores and casual_scores:
            mean_tourn = sum(tournament_scores) / len(tournament_scores)
            mean_casual = sum(casual_scores) / len(casual_scores)
            delta = mean_tourn - mean_casual

            if len(tournament_scores) < min_rounds or len(casual_scores) < min_rounds:
                delta *= scale_factor  # dampen due to insufficient data

            self.sand_bag_factor = delta
        else:
            self.sand_bag_factor = None
            print(f"Error in SB F : {self.name}, tournments : {len(tournament_scores)}, casual: {len(casual_scores)} ")


class PlayerRoundInfo:
    def __init__(self, player, tournament_name, round_number, handicap, tee, hole_scores,
                 total, net, tournament_flag=False, date=None, index=None, cr=None,
                 sr=None, course_played=None):
        self.player = player
        self.tournament_name = tournament_name
        self.tournament_flag = tournament_flag
        self.round_number = round_number
        self.handicap = handicap
        self.tee = tee
        self.hole_scores = hole_scores
        self.total = total
        self.net = net
        self.date = date
        self.index = index
        self.cr = cr
        self.sr = sr
        self.course_played = course_played
        self.duplicate = False
        self.completed = False

class Tournament:
    def __init__(self, name):
        self.name = name
        self.rounds = []

class Round:
    def __init__(self, tournament_name, round_number):
        self.tournament_name = tournament_name
        self.round_number = round_number
        self.player_rounds = []

class MMTeam:
    def __init__(self, name, player1, player2):
        self.name = name
        self.players = [player1, player2]
        self.aggregate_sand_bag_factor = None

    def compute_aggregate_sand_bag_factor(self):
        """
        Sum the sand_bag_factors of both players.
        """
        factors = [p.sand_bag_factor for p in self.players if p.sand_bag_factor is not None]
        self.aggregate_sand_bag_factor = sum(factors) if len(factors) == 2 else None

class CTeam:
    def __init__(self, name, mm_teams):
        if len(mm_teams) != 3:
            raise ValueError("A CTeam must have exactly 3 MMTeams.")
        self.name = name
        self.mm_teams = mm_teams
        self.aggregate_sand_bag_factor = None

    def compute_aggregate_score(self):
        """
        Use best 2 MMTeam sand_bag_factors (lower is better) to compute aggregate.
        """
        factors = [team.aggregate_sand_bag_factor for team in self.mm_teams
                   if team.aggregate_sand_bag_factor is not None]
        if len(factors) < 2:
            self.aggregate_sand_bag_factor = None
        else:
            self.aggregate_sand_bag_factor = sum(sorted(factors)[:2])




