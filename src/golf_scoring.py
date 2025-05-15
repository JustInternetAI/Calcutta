





# --- Course Setup ---
hole_handicap_ratings = [5, 13, 17, 3, 11, 9, 1, 15, 7, 10, 6, 18, 14, 2, 16, 4, 12, 8]
hole_pars = [4, 4, 3, 4, 3, 4, 4, 5, 4, 4, 4, 3, 5, 4, 3, 4, 5, 4]

# --- Convert net score to Stableford points ---
def stableford_points(net_score):
    if net_score >= 2:
        return -2  # Double bogey or worse
    elif net_score == 1:
        return 0   # Bogey
    elif net_score == 0:
        return 1   # Par
    elif net_score == -1:
        return 3   # Birdie
    elif net_score == -2:
        return 5   # Eagle
    else:
        return 7   # Double eagle or better


# --- Compute strokes received per hole ---
def strokes_received_per_hole(player_handicap):
    strokes = [0] * 18
    for i in range(18):
        hcap = hole_handicap_ratings[i]
        if player_handicap >= hcap:
            strokes[i] += 1
        if player_handicap > 18 and player_handicap >= hcap + 18:
            strokes[i] += 1
    return strokes

# --- Calculate Stableford points for a round ---
def calculate_stableford_round(player_round):
    if not player_round.hole_scores or len(player_round.hole_scores) != 18:
        return None

    gross_scores = player_round.hole_scores
    handicap = player_round.handicap
    strokes = strokes_received_per_hole(handicap)

    total_points = 0
    for i in range(18):
        try:
            gross_score = float(gross_scores[i])
        except (ValueError, TypeError):
            return None

        net = gross_score - strokes[i]
        net_relative_to_par = round(net - hole_pars[i])
        stableford = stableford_points(net_relative_to_par)

        total_points += stableford

    return total_points

# --- Compute strokes received per hole ---
def strokes_received_per_hole(player_handicap):
    strokes = [0] * 18
    for i in range(18):
        hcap = hole_handicap_ratings[i]
        if player_handicap >= hcap:
            strokes[i] += 1
        if player_handicap > 18 and player_handicap >= hcap + 18:
            strokes[i] += 1
    return strokes


