import streamlit as st
import pandas as pd
from collections import defaultdict

st.title("Calcutta Team Entry Interface")

# Initialize session state
if "all_players" not in st.session_state:
    st.session_state.all_players = []

if "pairs" not in st.session_state:
    st.session_state.pairs = []

if "teams" not in st.session_state:
    st.session_state.teams = []

st.header("1. Enter Player Names")
player_input = st.text_input("Enter a player name and click 'Add'")
if st.button("Add Player") and player_input:
    st.session_state.all_players.append(player_input.strip())
    st.success(f"Added {player_input.strip()}")

if st.session_state.all_players:
    st.subheader("Current Player List")
    st.write(st.session_state.all_players)

st.header("2. Create Pairs (Groups of 2)")
col1, col2 = st.columns(2)
with col1:
    p1 = st.selectbox("Select Player 1", options=[p for p in st.session_state.all_players])
with col2:
    p2 = st.selectbox("Select Player 2", options=[p for p in st.session_state.all_players if p != p1])

if st.button("Add Pair"):
    st.session_state.pairs.append((p1, p2))
    st.session_state.all_players.remove(p1)
    st.session_state.all_players.remove(p2)
    st.success(f"Added pair: {p1} & {p2}")

if st.session_state.pairs:
    st.subheader("Current Pairs")
    st.write(st.session_state.pairs)

st.header("3. Group Pairs into Teams (3 pairs per team)")
if len(st.session_state.pairs) >= 3:
    options = [f"{i+1}: {p1}, {p2}" for i, (p1, p2) in enumerate(st.session_state.pairs)]
    team_pair_indices = st.multiselect(
        "Select 3 pairs to form a team:",
        options=range(len(st.session_state.pairs)),
        format_func=lambda i: f"Pair {i+1}: {st.session_state.pairs[i][0]} & {st.session_state.pairs[i][1]}",
        max_selections=3
    )

    if len(team_pair_indices) == 3 and st.button("Create Team"):
        new_team = [st.session_state.pairs[i] for i in team_pair_indices]
        st.session_state.teams.append(new_team)
        for i in sorted(team_pair_indices, reverse=True):
            del st.session_state.pairs[i]
        st.success(f"Team created: {new_team}")

if st.session_state.teams:
    st.header("Final Calcutta Teams")
    for i, team in enumerate(st.session_state.teams):
        flat_team = [player for pair in team for player in pair]
        st.write(f"Team {i+1}: {flat_team}")
