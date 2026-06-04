# qss20-nba-engagement

## NBA Star Power and National TV Viewership

This project studies whether NBA star-player availability is associated with higher national television viewership during the 2023-24 regular season. The main outcome is `vwrs`, which measures average national TV viewership in thousands. The analysis compares viewership when specific All-Star players played versus when they did not, estimates player and matchup regressions with game-level controls, and uses a random forest model to estimate predicted viewership lift by player.

The project is observational, so the results should be interpreted as associations rather than causal effects. Many high-profile players appear in games that are already selected for national television, involve popular teams, or fall in stronger broadcast windows, so player estimates may reflect both star power and scheduling context.

## Research Questions

1. Which NBA stars are associated with the largest increases in national TV viewership?
2. How does viewership differ when a player plays compared with when that same player misses games involving his own team?
3. Which opposing-star matchups are associated with higher national TV viewership after controlling for team quality, betting market expectations, holiday games, and team valuation?
4. Can player availability and game-level controls help predict national TV viewership better than a simple baseline model?

## Repository Structure

```text
qss20-nba-engagement/
├── code/                  # Python scripts used for cleaning, analysis, modeling, and figures
├── data/                  # Raw, cleaned, and analysis-ready CSV files
├── output/                # Figures and other generated outputs
└── README.md              # Project overview and reproducibility guide
```

## Data Files

| File | Description | Used by |
|---|---|---|
| [`data/ratings_final_allstar_indicators.csv`](data/ratings_final_allstar_indicators.csv) | Game-level national TV dataset with team names, viewership, betting controls, style variables, and All-Star played indicators. | `00_merge_team_valuation.py` |
| [`data/team_valuation_game_level.csv`](data/team_valuation_game_level.csv) | Game-level file with `GAME_ID` and average team valuation in billions. | `00_merge_team_valuation.py` |
| [`data/qss20_finalds.csv`](data/qss20_finalds.csv) | Final merged game-level analysis dataset. This is the main input for the descriptive, regression, and prediction scripts. | `01`, `02`, `03`, `04` |
| [`data/player_viewership_differences.csv`](data/player_viewership_differences.csv) | Player-level descriptive output comparing average viewership when each player played versus did not play. | `05_website_figures.py` |
| [`data/team_specific_player_viewership.csv`](data/team_specific_player_viewership.csv) | Team-specific descriptive output comparing viewership in a player's own team games when he played versus missed. | `05_website_figures.py` |
| [`data/player_regression_results.csv`](data/player_regression_results.csv) | One-player-at-a-time OLS regression results using log viewership as the outcome. | Final paper / tables |
| [`data/matchup_regression_results.csv`](data/matchup_regression_results.csv) | OLS regression results for selected opposing-star matchup indicators. | Final paper / tables |
| [`data/prediction_lift_model_evaluation.csv`](data/prediction_lift_model_evaluation.csv) | Cross-validated random forest evaluation metrics and baseline comparison. | Final paper / tables |
| [`data/prediction_lift_by_player.csv`](data/prediction_lift_by_player.csv) | Player-level predicted viewership lift from the random forest model. | `05_website_figures.py`, final paper |

## Code Files: Inputs, Purpose, and Outputs

Run the scripts in numerical order. Each script is written so that the file paths match the repository folder structure.

| Script | Inputs | What it does | Outputs |
|---|---|---|---|
| [`code/00_merge_team_valuation.py`](code/00_merge_team_valuation.py) | `data/ratings_final_allstar_indicators.csv`; `data/team_valuation_game_level.csv` | Merges average team valuation into the main ratings and All-Star indicator dataset using `GAME_ID`. Checks for required columns, duplicate game IDs, row-count changes, and missing valuation values. | `data/qss20_finalds.csv` |
| [`code/01_player_viewership_descriptives.py`](code/01_player_viewership_descriptives.py) | `data/qss20_finalds.csv` | Finds all player indicator columns ending in `_played`. For each player, compares average viewership when the player played to average viewership when the player did not play across the full national TV sample. | `data/player_viewership_differences.csv` |
| [`code/02_team_specific_player_viewership_descriptives.py`](code/02_team_specific_player_viewership_descriptives.py) | `data/qss20_finalds.csv` | Compares viewership only within games involving each player's own team. This avoids comparing a player playing for his team to unrelated games between other teams. | `data/team_specific_player_viewership.csv` |
| [`code/03_player_matchup_regressions.py`](code/03_player_matchup_regressions.py) | `data/qss20_finalds.csv` | Creates `log_vwrs`, runs one-player-at-a-time OLS regressions with robust HC3 standard errors, and estimates selected opposing-star matchup regressions. Player regressions control for `avg_net_rating`, `spread`, `holiday`, and `total`. Matchup regressions also include `avg_team_valuation_bil`. | `data/player_regression_results.csv`; `data/matchup_regression_results.csv` |
| [`code/04_random_forest.py`](code/04_random_forest.py) | `data/qss20_finalds.csv` | Fits a random forest model predicting `vwrs` using player indicators with at least 10 appearances plus game-level controls. Uses 5-fold cross-validated predictions, compares performance to a baseline mean-prediction model, and estimates each player's predicted viewership lift. | `data/prediction_lift_model_evaluation.csv`; `data/prediction_lift_by_player.csv`; `output/prediction_lift_by_player.png` |
| [`code/05_website_figures.py`](code/05_website_figures.py) | `data/player_viewership_differences.csv`; `data/team_specific_player_viewership.csv` | Creates presentation-ready figures for the project website and lightning talk. The figures show top descriptive viewership lifts and played-versus-missed viewership gaps. | `output/fig1_top_player_viewership_lift.png`; `output/fig2_team_specific_viewership_lift.png`; `output/fig3_played_vs_missed_viewership.png` |

## Main Outputs

| Output | Description |
|---|---|
| [`output/fig1_top_player_viewership_lift.png`](output/fig1_top_player_viewership_lift.png) | Bar chart of players associated with the largest descriptive national viewership increases. |
| [`output/fig2_team_specific_viewership_lift.png`](output/fig2_team_specific_viewership_lift.png) | Bar chart of team-specific viewership increases when a player played versus missed games involving his own team. |
| [`output/fig3_played_vs_missed_viewership.png`](output/fig3_played_vs_missed_viewership.png) | Dot-and-line chart comparing average viewership when selected players played versus missed. |
| [`output/prediction_lift_by_player.png`](output/prediction_lift_by_player.png) | Random forest predicted viewership lift by player. |

## How to Reproduce the Analysis

From the project root directory, run:

```bash
python code/00_merge_team_valuation.py
python code/01_player_viewership_descriptives.py
python code/02_team_specific_player_viewership_descriptives.py
python code/03_player_matchup_regressions.py
python code/04_random_forest.py
python code/05_website_figures.py
```

The scripts create or update files in `data/` and `output/`. The most important final dataset is `data/qss20_finalds.csv`, and the most important final model outputs are `data/player_regression_results.csv`, `data/matchup_regression_results.csv`, `data/prediction_lift_model_evaluation.csv`, and `data/prediction_lift_by_player.csv`.

## Required Python Packages

The analysis uses the following Python packages:

```text
pandas
numpy
matplotlib
statsmodels
scikit-learn
```

## Methods Summary

The project uses three types of analysis. First, descriptive comparisons calculate the difference in average viewership when each player played versus when he did not. Second, OLS regressions estimate player and matchup associations with log viewership while controlling for game-level context. Third, a random forest model predicts viewership using player indicators and controls, then uses cross-validated predictions to estimate each player's predicted viewership lift. The random forest evaluation also compares model error to a baseline model that always predicts average viewership.

## Notes on Interpretation

- `vwrs` is measured in thousands of viewers.
- Player indicators equal 1 when the player appeared in the game and 0 otherwise.
- Descriptive differences do not control for opponent, team popularity, broadcast slot, or other scheduling factors.
- Regression and random forest models include selected game-level controls, but they still do not prove causal effects.
- Players with very few appearances are excluded from the random forest lift chart so that the estimates are not driven by extremely small samples.
