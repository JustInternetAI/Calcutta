# golf_utils.py
import pickle
from difflib import get_close_matches, SequenceMatcher

def compute_all_sandbag_factors(players, min_rounds=5, scale_factor=0.5):
    """
    Compute sand_bag_factor for each player using their existing rounds.
    
    Args:
        players (dict[str, Player]): Mapping from player name to Player object.
        min_rounds (int): Minimum rounds of each type to trust full difference.
        scale_factor (float): Dampening factor for small sample sizes.
    """
    print(f"Calculating {len(players)} players")
    for player in players.values():
        player.compute_sand_bag_factor(min_rounds=min_rounds, scale_factor=scale_factor)
        #print(f"Name : {player.name}, SB Factor: {player.sand_bag_factor}")




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
    

