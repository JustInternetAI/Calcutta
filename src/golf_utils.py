# golf_utils.py
import pickle
from difflib import get_close_matches, SequenceMatcher
import sys
from pathlib import Path
import importlib
import pandas as pd

from math import comb
from typing import Dict
from scipy.stats import mannwhitneyu, ttest_ind, shapiro, levene
import numpy as np


# Reload golf_classes FIRST
import golf_classes


# THEN import the class definitions
from golf_classes import Player, PlayerRoundInfo, Tournament, Round, MMTeam, CTeam


def compute_all_sandbag_factors(players, min_rounds=5, scale_factor=0.5):
    """
    Compute sand_bag_factor for each player using their existing rounds.
    
    Args:
        players (dict[str, Player]): Mapping from player name to Player object.
        min_rounds (int): Minimum rounds of each type to trust full difference.
        scale_factor (float): Dampening factor for small sample sizes.
    """
    print(f"Calculating {len(players)} players")
    errorCount = 0
    passCount = 0
    for player in players.values():
        player.compute_sand_bag_factor(min_rounds=min_rounds, scale_factor=scale_factor)
        if player.sand_bag_factor is None:
            errorCount = errorCount + 1
        else:
            passCount = passCount + 1
        #print(f"Name : {player.name}, SB Factor: {player.sand_bag_factor}")

    return passCount, errorCount




def save_pickle(data, filepath):
    if isinstance(data, dict) and not any(data.values()):
        print(f"⚠️ Warning: Saving mostly empty dictionary to {filepath}")
    with open(filepath, 'wb') as f:
        pickle.dump(data, f)
        print(f"✅ Saved to {filepath}")


def load_pickle(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = pickle.load(f)
            print(f"✅ Loaded from {filepath}")
            return data
    except FileNotFoundError:
        print(f"⚠️ File not found: {filepath}")
        return None


def get_player_by_name(name, players, fuzzy=False):
    """
    Normalize the input name and match it against the players dictionary.

    Args:
        name (str): The name to look up.
        players (dict[str, Player]): Dictionary of known Player objects.
        fuzzy (bool): If True, use fuzzy matching when exact normalized match fails.

    Returns:
        Player object if found, else None.
    """
    normalized_name = name.strip().lower()
    normalized_lookup = {
        p_name.strip().lower(): p_obj for p_name, p_obj in players.items()
    }

    result = normalized_lookup.get(normalized_name)
    if result is None and fuzzy:
        close = get_close_matches(normalized_name, normalized_lookup.keys(), n=1, cutoff=0.8)
        if close:
            return normalized_lookup[close[0]]
    return result



def get_close_player_matches(name, players, n=5, cutoff=0.7):
    """
    Return a list of closely matching players based on fuzzy string comparison.

    Args:
        name (str): Name to match against the player list.
        players (dict[str, Player]): Dictionary of known Player objects.
        n (int): Max number of matches to return.
        cutoff (float): Similarity threshold (0 to 1).

    Returns:
        List of tuples: (match_score, player_name, Player object), sorted by score descending.
    """
    normalized_name = name.strip().lower()
    candidate_list = [(p_name.strip().lower(), p_obj) for p_name, p_obj in players.items()]

    scored_matches = []
    for player_name, player_obj in candidate_list:
        score = SequenceMatcher(None, normalized_name, player_name).ratio()
        if score >= cutoff:
            scored_matches.append((score, player_name, player_obj))

    scored_matches.sort(reverse=True, key=lambda x: x[0])
    return scored_matches[:n]


def rebind_team_players(players, mm_teams, c_teams):
    """
    Rebind Player objects in mm_teams and c_teams to the canonical Player instances from `players`.

    Args:
        players (dict[str, Player]): Canonical mapping of player name to Player object.
        mm_teams (dict[str, MMTeam]): Mapping of team name to MMTeam object.
        c_teams (dict[str, CTeam]): Mapping of team name to CTeam object.
    """
    fix_count = 0
    for mm_team in mm_teams.values():
        fixed_players = []
        for player in mm_team.players:
            canonical = players.get(player.name)
            if canonical and canonical is not player:
                fix_count += 1
            fixed_players.append(canonical or player)
        mm_team.players = fixed_players

    for c_team in c_teams.values():
        for i, mm_team in enumerate(c_team.mm_teams):
            if isinstance(mm_team, MMTeam):
                fixed_mm_players = []
                for player in mm_team.players:
                    canonical = players.get(player.name)
                    if canonical and canonical is not player:
                        fix_count += 1
                    fixed_mm_players.append(canonical or player)
                mm_team.players = fixed_mm_players
                c_team.mm_teams[i] = mm_team  # reassign to be safe

    print(f"🔁 Rebound {fix_count} player references to canonical Player objects.")
    


def score_randomness_test(player,
                          alt: str = "less",
                          min_len: int = 5
                         ) -> Dict[str, float | None]:
    """
    Return one-tailed p-values that tournament scores are randomly drawn
    from the same distribution as casual scores (shifted lower).

    Keys in the result:
        'n_t', 'n_c'          – sample sizes
        'p_mwu'               – Mann-Whitney U p-value               (exact)
        'p_ttest'             – Welch t-test p-value                 (approx)
        'p_all_lower'         – Pr(all T scores < all C scores)      (exact)
    """
    ts = np.array([r.net for r in player.rounds if r.tournament_flag and r.net is not None])
    cs = np.array([r.net for r in player.rounds if not r.tournament_flag and r.net is not None])
    n_t, n_c = len(ts), len(cs)

    if n_t < 2 or n_c < 2:
        return {"error": "Need at least 2 scores in each cohort."}

    # 1) Mann–Whitney U (rank-sum) — exact for small n
    p_mwu = mannwhitneyu(ts, cs, alternative=alt).pvalue

    # 2) Welch one-tailed t-test if data look ~normal
    p_ttest = None
    if n_t >= min_len and n_c >= min_len:
        norm_ok = (shapiro(ts).pvalue > 0.05) and (shapiro(cs).pvalue > 0.05)
        var_ok  = levene(ts, cs).pvalue > 0.05
        if norm_ok and var_ok:
            p_ttest = ttest_ind(ts, cs, equal_var=False, alternative=alt).pvalue

    # 3) Exact probability that **all** T < all C under H0
    #    = 1 / C(n_t + n_c, n_t)
    p_all_lower = 1 / comb(n_t + n_c, n_t)

    return dict(n_t=n_t, n_c=n_c, p_mwu=p_mwu, p_ttest=p_ttest, p_all_lower=p_all_lower)

def sandbag_report(stats: dict,
                   player_name: str | None = None,
                   alpha: float = 0.05) -> str:
    """
    Render a friendly one-liner plus legend from the stats dict.
    Formats very small probabilities so they never round to 0.0 %.
    """
    if "error" in stats:
        return stats["error"]

    # ----- helpers ---------------------------------------------------------
    def fmt_pct(p: float) -> str:
        """Pretty percentage with adaptive precision."""
        pct = p * 100
        if pct >= 0.1:         # 0.1 % – 100 %   → one decimal
            return f"{pct:.1f} %"
        elif pct >= 0.01:      # 0.01 % – 0.1 %  → two decimals
            return f"{pct:.2f} %"
        elif pct >= 0.0001:    # 0.0001 % – 0.01 % → four decimals
            return f"{pct:.4f} %"
        else:                  # smaller than 1 in a million
            return f"{pct:.1e} %"

    def fmt_p(p: float | None) -> str:
        return f"{p:.3g}" if p is not None else "—"

    # -----------------------------------------------------------------------
    p_mwu   = stats["p_mwu"]
    p_ttest = stats.get("p_ttest")
    p_all   = stats["p_all_lower"]

    name = f"{player_name} – " if player_name else ""
    headline = (
        f"{name}possible sandbagging: only {fmt_pct(p_mwu)} probability this is random chance"
        if p_mwu < alpha else
        f"{name}no evidence of sandbagging: {fmt_pct(p_mwu)} probability pattern is random"
    )

    lines = [
        headline,
        f"   • Mann-Whitney U p = {fmt_p(p_mwu)}  (rank-based, distribution-free)",
        (
            f"   • Welch t-test   p = {fmt_p(p_ttest)}  (parametric, one-tailed)"
            if p_ttest is not None else
            "   • Welch t-test   – skipped (sample too small or not normal)"
        ),
        f"   • P(all T < C)   = {fmt_pct(p_all)}  "
        "(exact probability every tournament score beats every casual score)"
    ]
    return "\n".join(lines)


from math import log10
from typing import List, Dict

def top_sandbaggers(players: Dict[str, Player],
                    n: int = 10,
                    alpha: float = 0.05,
                    min_rounds: int = 2,
                    alt: str = "less") -> List[dict]:
    """
    Find the N players whose tournament scores look *most* suspiciously low.

    Returns a list of dicts sorted by smallest p_mwu:
       [{
         'name': str,
         'stats': { … },          # full score_randomness_test result
         'suspicion_score': float # -log10(p_mwu) for easy comparison
       }, …]
    """

    ranked = []
    for name, player in players.items():

        stats = score_randomness_test(player, alt=alt)
        if "error" in stats:
            continue                      # skip players without enough data

        # Require a minimal sample size to avoid noise
        if stats['n_t'] < min_rounds or stats['n_c'] < min_rounds:
            continue

        p = stats["p_mwu"]
        if p < alpha:                     # suspicious
            ranked.append({
                "name": name,
                "stats": stats,
                "suspicion_score": -log10(p)   # bigger = more suspicious
            })

    # sort by strongest evidence first
    ranked.sort(key=lambda x: x["stats"]["p_mwu"])
    return ranked[:n]


def print_top_sandbaggers(players: Dict[str, Player],
                          n: int = 10,
                          alpha: float = 0.05):
    """Pretty-print the top N sandbaggers."""
    suspects = top_sandbaggers(players, n=n, alpha=alpha)
    if not suspects:
        print("✅ No players meet the sandbagging threshold.")
        return

    print(f"🚩 Top {len(suspects)} possible sandbaggers (α = {alpha}):\n")
    for idx, s in enumerate(suspects, 1):
        print(f"{idx}. {sandbag_report(s['stats'], player_name=s['name'], alpha=alpha)}\n")



