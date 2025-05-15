📄 Calcutta Prediction Project Status

🎯 Project Goal

Predict value in Calcutta golf tournaments by comparing auction price vs. win probability.

📂 Data Available

✅ 3 years of historical Calcutta tournament results.
✅ Individual player scores and handicaps (~20 rounds per player last year).
✅ Calcutta team compositions (3 MM teams per C team; Day 2 scores are best 2 MM teams combined Stableford).
✅ Tee information per player (course rating, slope, course handicap).
✅ Auction sale prices per team.
🏌 Competition Rules Summary

Draft: Snake draft, order based on Day 1 scores.
Team Composition: Fixed after draft.
Day 2 Scoring: Best 2 of 3 MM teams (Stableford, handicap adjusted). Each MM team's score is the sum of 2 players' Stableford scores.
🛠️ System Status

📂 Data ingestion from Excel spreadsheets (.xlsx, .xlsm).
🧹 Data cleaning mostly complete (standardized names, scores, handicaps).
🧩 Python modules created (golf_classes.py for core classes).
💾 Objects serialized with Pickle (shared across notebooks).
🔗 GitHub repo set up and used actively.
💻 Environment

📓 Jupyter Notebooks (local, Ubuntu and Mac).
🐍 Python (Conda env).
🎮 RTX 3090 GPU (Ubuntu machine, optional for heavy computations later).
🔗 GitHub for version control.
⚡ Key Challenges

📈 Modeling player variance vs. handicap (especially under tournament pressure).
🧠 Simulating snake draft effects based on Day 1 scores.
🛠️ Handling missing/incomplete older tournament data.
📋 Assumptions

Handicaps reflect player skill.
Draft and team composition are consistent year-to-year.
No unaccounted external events (injury, weather) unless data shows otherwise.
🔮 Current Status

✅ Player data in Pickle format, with C teams, hole-by-hole data (where available), and aggregate Gross, Net, etc.
✅ Methods to inspect player data and graph performance built.
🚀 Next Major Steps

Estimate Stableford scores for rounds with only Gross, Net, and handicap data.
Build tournament adjustment factors per player (capture “plays better/worse than handicap in tournaments”).
Finalize player performance model (simple random sampling vs. weighted by variance factors).
Implement Monte Carlo simulation engine for Day 2 team scoring.
Calculate team win probabilities from simulations.
Compare team valuations to auction prices.
Build valuation reports (basic table + optional visualization in notebooks).