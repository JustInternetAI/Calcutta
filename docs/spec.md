# 📄 Calcutta Prediction Project - System Specification

## 🎯 Objective
Develop a system to predict **team win probabilities** in Calcutta golf tournaments and identify **overvalued/undervalued teams** by comparing auction prices to simulation-based valuations.

---

## 🗺️ System Overview

### Data Sources
- **Tournament Data**  
  - Results (gross, net, handicaps)  
  - Team compositions  
  - Auction prices  

- **Player Data**  
  - Hole-by-hole scores (partial)  
  - Aggregate gross/net scores  
  - Handicap Index  
  - Course rating, slope, course handicap  

### Modeling Assumptions
- Player handicaps reflect true skill.
- Player performance is influenced by variance and tournament adjustment factor.
- Snake draft and Day 2 scoring rules are consistent across years.
- Missing data is handled using best-effort approximations (e.g., estimating Stableford from gross/net).

---

## 🔧 System Components

### 1. **Data Preparation**
- Clean and standardize all historical tournament and player data.
- Create structured classes for players, teams, and tournaments.
- Serialize data using Pickle for fast access.

### 2. **Player Performance Modeling**
- Estimate Stableford scores for rounds lacking hole-by-hole data.
- Create player-specific tournament adjustment factors (e.g., plays better/worse vs. handicap in tournaments).
- Build sampling model to simulate player rounds using historical data with adjustments.

### 3. **Tournament Simulation Engine**
- Simulate Day 2 using Monte Carlo:
  - For each simulation:
    - Simulate individual player scores.
    - Calculate MM team scores (sum of 2 players).
    - Calculate C team scores (best 2 of 3 MM teams).
- Repeat many times to produce win probabilities for each team.

### 4. **Value Analysis**
- Calculate EV and ROI using predicted win probabilities and actual auction prices.
- Rank teams by value.

### 5. **Reporting and Visualization**
- Generate reports with simulation outcomes and team valuations.
- Visualize simulation outputs (optional).
- Export results in easy-to-share formats.

---

## 🔮 Stretch Goals
- Simulate snake draft dynamics based on Day 1 scores (impact of Day 1 performance on auction values and team strength).
- Incorporate environmental or external data (weather, injuries) if available.
- Explore GPU acceleration for faster simulations using RTX 3090.

---

## 🛡️ Key Assumptions and Risks
- **Data completeness and accuracy**: Missing or incorrect historical data may affect model fidelity.
- **Handicap adjustments**: Players may consistently over/underperform handicaps in tournaments; adjustment factors attempt to model this.
- **Draft strategy simulation**: Initially modeled as simple snake draft; more complex draft behaviors (biases, mistakes) are outside scope unless data supports modeling them.

---

## 🚀 Tech Stack
- **Python (Conda environment)**
- **Jupyter Notebooks (local)**
- **Pandas, NumPy, Matplotlib, Pickle**
- **GitHub for version control**
- **Optional: CUDA with RTX 3090 for heavy computations**

