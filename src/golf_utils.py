# golf_utils.py

def postprocess_players(players, scoring_func):
    for player in players.values():
        # Fix missing attribute for old pickled objects
        if not hasattr(player, '_stableford_stats'):
            player._stableford_stats = None

        player.compute_stableford_stats(scoring_func=scoring_func)