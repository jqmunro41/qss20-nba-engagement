# qss20-nba-engagement

# NBA Style of Play, Star Power, and Audience Engagement

## Project Summary

This project examines what drives audience engagement with NBA games. I am currently considering two related research questions. First, I may investigate which specific star players drive the most engagement with nationally televised NBA games. Second, I may examine whether different style-of-play predictors explain highlight viewership and national TV viewership differently.

The broader motivation is that NBA engagement may depend on both who is playing and how the game is played. Star players may attract viewers because of name recognition, while certain styles of play, such as three-point shooting, fast pace, dunks, or other highlight plays, may be more important for YouTube engagement.

## Research Questions

This project is currently focused on one of two possible directions:

1. **Star player engagement question:**  
   Which NBA star players are most strongly associated with higher audience engagement?

2. **Style-of-play engagement question:**  
   Which style-of-play variables better predict YouTube highlight viewership compared with national TV viewership?

The first question focuses on player-specific effects, while the second compares different forms of fan engagement. National TV viewership may be driven more by team quality, star power, and broadcast context, while YouTube highlight viewership may be more responsive to exciting or highlight-friendly styles of play.

## Data

This repository currently includes two main datasets:

- `ratings_final_allstar_indicators.csv`: game-level national TV ratings data with added indicator variables for whether specific All-Star players played in each game.
- `nba_highlights_final.csv`: game-level YouTube highlight data, including engagement measures such as video views, likes, and comments.

The ratings dataset is useful for analyzing national TV viewership. The highlights dataset is useful for analyzing digital engagement with NBA game highlights.

## Repository Structure

- `data/`: contains the project datasets.
- `code/`: contains scripts and notebooks used to load, clean, and analyze the data.
- `output/`: contains figures and tables generated from the analysis.

## Code Files

- `NBA_stats.ipynb`: notebook used to collect, clean, and organize NBA statistical data.
- `figures.r`: R script used to create preliminary descriptive figures.

## Preliminary Outputs

The repository currently includes preliminary figures related to the project, including:

- A figure showing total games missed by All-Stars per season.
- A figure comparing NBA viewership and three-point attempt rate over time.

These figures are exploratory and help motivate the project. The All-Star absences figure relates to the player availability and star power question. The three-point shooting and viewership figure relates to the style-of-play question.

## Current Progress

So far, I have:

- Collected and organized national TV ratings data.
- Added player-specific All-Star indicator variables to the ratings dataset.
- Collected YouTube highlight engagement data.
- Created preliminary figures related to star availability, three-point shooting, and viewership.
- Begun organizing the repository into separate folders for data, code, and output.

## Planned Next Steps

Next, I plan to narrow the project toward one main research question. If I focus on star players, I will estimate which All-Star indicators are most strongly associated with TV viewership or highlight engagement. If I focus on style of play, I will compare predictors of YouTube highlight views and national TV viewership using variables such as pace, three-point attempt rate, fastbreak scoring, dunks, and other highlight-related measures.

The final analysis will likely use regression models and/or machine learning methods to compare which variables are most predictive of different forms of NBA audience engagement.
