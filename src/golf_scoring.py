
import random

# Define the outcome probabilities by handicap bracket (from your chart)
HANDICAP_PROFILES = {
    (0, 0): {'birdie': 2.4, 'par': 9.7, 'bogey': 4.4, 'dbogey': 1.0, 'tbogey': 0.5},
    (1, 5): {'birdie': 1.5, 'par': 9.0, 'bogey': 5.9, 'dbogey': 1.3, 'tbogey': 0.3},
    (6, 10): {'birdie': 0.9, 'par': 7.0, 'bogey': 7.3, 'dbogey': 2.3, 'tbogey': 0.5},
    (11, 15): {'birdie': 0.5, 'par': 5.1, 'bogey': 7.7, 'dbogey': 3.5, 'tbogey': 1.1},
    (16, 20): {'birdie': 0.3, 'par': 3.6, 'bogey': 7.3, 'dbogey': 4.7, 'tbogey': 2.1},
    (21, 25): {'birdie': 0.2, 'par': 2.5, 'bogey': 6.3, 'dbogey': 5.5, 'tbogey': 3.4},
    (26, 30): {'birdie': 0.1, 'par': 1.7, 'bogey': 5.2, 'dbogey': 5.9, 'tbogey': 5.1},
    (31, 35): {'birdie': 0.1, 'par': 1.2, 'bogey': 4.2, 'dbogey': 5.7, 'tbogey': 6.8},
    (36, 99): {'birdie': 0.05, 'par': 0.7, 'bogey': 2.9, 'dbogey': 4.8, 'tbogey': 9.5},
}

# Stableford points (net scoring)
STABLEFORD_POINTS = {
    'birdie': 3,
    'par': 1,
    'bogey': 0,
    'dbogey': -2,
    'tbogey': -2,  # Triple bogey or worse same as double bogey in your system
}

# --- Convert net score to Stableford points ---
def stableford_points(net_to_par):
    if net_to_par >= 2:
        return -2  # Double bogey or worse
    elif net_to_par == 1:
        return 0   # Bogey
    elif net_to_par == 0:
        return 1   # Par
    elif net_to_par == -1:
        return 3   # Birdie
    elif net_to_par == -2:
        return 5   # Eagle
    else:
        return 7   # Double eagle or better


# --- Course Setup ---
#hole_handicap_ratings = [5, 13, 17, 3, 11, 9, 1, 15, 7, 10, 6, 18, 14, 2, 16, 4, 12, 8]
hole_pars = [4, 4, 3, 4, 3, 4, 4, 5, 4, 4, 4, 3, 5, 4, 3, 4, 5, 4]

# Hole stroke index 1-18 (hardest to easiest)
HOLE_STROKE_INDEX = {
    1: 5, 2: 13, 3: 17, 4: 3, 5: 11, 6: 9, 7: 1, 8: 15, 9: 7,
    10: 10, 11: 6, 12: 18, 13: 14, 14: 2, 15: 16, 16: 4, 17: 12, 18: 8
}


def get_handicap_profile(course_handicap):
    """Find matching profile by course handicap."""
    for lower, upper in HANDICAP_PROFILES:
        if lower <= course_handicap <= upper:
            return HANDICAP_PROFILES[(lower, upper)]
    return HANDICAP_PROFILES[(36, 99)]  # Default to highest bracket if over 99

def select_hole_outcome(profile):
    """Randomly select an outcome using weighted probabilities."""
    outcomes = list(profile.keys())
    weights = list(profile.values())
    return random.choices(outcomes, weights=weights, k=1)[0]


def strokes_allocated_per_hole(course_handicap):
    """Calculate strokes per hole accounting for handicaps >18."""
    strokes_per_hole = {}
    for hole, stroke_index in HOLE_STROKE_INDEX.items():
        strokes = 1 if course_handicap >= stroke_index else 0
        if course_handicap > 18 and course_handicap - 18 >= stroke_index:
            strokes += 1
        strokes_per_hole[hole] = strokes
    return strokes_per_hole



def adjust_for_handicap(gross_strokes, strokes_allocated, hole_type, reduction_factor=0.7):
    """Probabilistic reduction for triple bogey holes."""
    if hole_type == 'tbogey' and strokes_allocated > 0:
        if random.random() <= reduction_factor:
            return gross_strokes - strokes_allocated
        else:
            return gross_strokes  # No reduction
    else:
        return gross_strokes - strokes_allocated

def simulate_round(course_handicap):
    """Simulate a full 18-hole round with randomized hole outcomes and net Stableford scoring."""
    profile = get_handicap_profile(course_handicap)
    strokes_per_hole = strokes_allocated_per_hole(course_handicap)
    total_stableford = 0

    for hole in range(1, 19):
        outcome = select_hole_outcome(profile)
        gross_strokes = hole_pars[hole - 1] + {
            'birdie': -1,
            'par': 0,
            'bogey': 1,
            'dbogey': 2,
            'tbogey': 3
        }[outcome]

        net_strokes = adjust_for_handicap(gross_strokes, strokes_per_hole[hole], outcome)
        net_to_par = net_strokes - hole_pars[hole-1]

        total_stableford += stableford_points(net_to_par)

    return total_stableford


def compute_real_stableford(rnd):
    strokes_per_hole = strokes_allocated_per_hole(rnd.handicap)
    total_stableford = 0
    for hole in range(1, 19):
        gross_strokes = rnd.hole_scores[hole - 1]  # list is 0-indexed
        net_strokes = gross_strokes - strokes_per_hole[hole]  # dict is 1-indexed
        net_to_par = net_strokes - hole_pars[hole - 1]  # list is 0-indexed
        total_stableford += stableford_points(net_to_par)
    return total_stableford



CALIBRATION_CORRECTIONS = {
    (0, 4): 2.46,
    (5, 9): 2.00,
    (10, 14): 3.05,
    (15, 19): 6.83,
    (20, 24): 1.26,
    (25, 29): -0.29,
    (30, 34): -0.15,
    (35, 39): 2.37,
    (40, 99): 0.55
}

def calibrated_simulate_round(course_handicap):
    simulated_score = simulate_round(course_handicap)
    for (low, high), correction in CALIBRATION_CORRECTIONS.items():
        if low <= course_handicap <= high:
            return simulated_score + correction
    return simulated_score  # fallback if no band found












