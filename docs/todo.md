# ✅ Calcutta Prediction Project - TODO Checklist

## 📄 Data Preparation
- [x] Ingest historical tournament data (results, auction prices, team compositions).
- [x] Ingest individual player data (scores, handicaps, tee information).
- [x] Clean data (standardize names, handle missing data, correct inconsistencies).
- [x] Create Player and Tournament classes.
- [x] Serialize data using Pickle for easy reuse.

## 📊 Player Performance Modeling
- [ ] Build function to estimate Stableford scores from Gross/Net/Handicap data.
- [ ] Create player tournament performance adjustment factors (better/worse vs. handicap).
- [ ] Analyze variance of player scores historically and under tournament conditions.
- [ ] Decide on player sampling method (simple random vs. weighted by variance and adjustment factor).
- [ ] Validate performance models using past tournaments.

## 🎲 Simulation System
- [ ] Build Monte Carlo engine to simulate Day 2 team scores.
- [ ] Incorporate team composition rules (best 2 of 3 MM teams, each MM team sum of 2 players' Stableford).
- [ ] Simulate many tournaments to generate win probability distributions for all teams.
- [ ] Implement snake draft simulation based on Day 1 scores (optional refinement).
- [ ] Validate simulation engine against known historical outcomes.

## 💰 Value Analysis
- [ ] Compare auction prices vs. predicted win probabilities.
- [ ] Calculate value metrics (e.g., EV per dollar spent, ROI rankings).
- [ ] Highlight overvalued/undervalued teams.

## 📊 Visualization and Reporting (Optional)
- [ ] Create notebook with team valuations table.
- [ ] Add basic visualizations (e.g., histograms of simulated finishes, value vs. price scatter plots).
- [ ] Export report as PDF or HTML for easy review.

## 🛠️ System Maintenance and Enhancements (Future)
- [ ] Automate data ingestion for new tournaments.
- [ ] Improve robustness of draft simulation (account for snake draft strategies).
- [ ] Explore use of GPU acceleration for simulations (RTX 3090).
- [ ] Document code and workflow in README.md.
