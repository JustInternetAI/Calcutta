# golf_classes.py

import numpy as np
from typing import List, Dict, Optional
from dataclasses import dataclass


class Player:
    def __init__(self, name):
        self.name = name
        self.rounds = []
        self._stableford_stats = None  # lazy cache

    def compute_stableford_stats(self, scoring_func):
        """
        Compute and cache the player's Stableford scores using a provided scoring function.
        
        Args:
            scoring_func: a function that takes a PlayerRoundInfo object and returns a Stableford score
        """
        scores = [scoring_func(rnd) for rnd in self.rounds]
        scores = [s for s in scores if s is not None]

        if scores:
            avg = np.mean(scores)
            std = np.std(scores)
        else:
            avg = std = 0.0

        self._stableford_stats = {
            "scores": scores,
            "average": avg,
            "stddev": std
        }

    @property
    def stableford_average(self):
        if self._stableford_stats is None:
            raise ValueError("Stableford stats not computed. Call compute_stableford_stats(scoring_func) first.")
        return self._stableford_stats["average"]

    @property
    def stableford_stddev(self):
        if self._stableford_stats is None:
            raise ValueError("Stableford stats not computed. Call compute_stableford_stats(scoring_func) first.")
        return self._stableford_stats["stddev"]

    @property
    def stableford_scores(self):
        if self._stableford_stats is None:
            raise ValueError("Stableford stats not computed. Call compute_stableford_stats(scoring_func) first.")
        return self._stableford_stats["scores"]

class PlayerRoundInfo:
    def __init__(self, player, tournament_name, round_number, handicap, tee, hole_scores, total, net, date=None , index = None, cr = None, sr = None, course_played = None):

        self.player = player # Golfer name
        self.tournament_name = tournament_name
        self.round_number = round_number
        self.handicap = handicap # course handicap
        self.tee = tee
        self.hole_scores = hole_scores  # List of 18 scores
        self.total = total # gross score
        self.net = net
        self.date = date
        self.index = index #player index
        self.cr = cr # course rating
        self.sr = sr # course slope rating
        self.course_played = course_played
        self.duplicate = False  
        self.completed = False

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