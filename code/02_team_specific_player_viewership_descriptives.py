#!/usr/bin/env python
# coding: utf-8

# In[10]:


"""
02_team_specific_player_viewership.py

Purpose:
    Compare average NBA game viewership when each selected all-star player played
    versus when that same player missed games involving his own team.

Input:
    data/qss20_finalds.csv
        Final game-level dataset with ratings, all-star indicators, team names,
        and other controls.

Output:
    data/team_specific_player_viewership.csv
        Player-level summary comparing viewership in team games when each player
        played versus missed.
"""

import pandas as pd


# Functions

def load_data(file_path):
    """
    Load the final dataset and print basic diagnostics.
    """
    df = pd.read_csv(file_path)

    print(f"\nLoaded file: {file_path}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    return df


def check_required_columns(df, required_columns, dataset_name):
    """
    Check that required columns are present in the dataset.
    """
    missing_columns = []

    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        raise ValueError(
            f"{dataset_name} is missing these required columns: {missing_columns}"
        )


def get_player_team_dictionary():
    """
    Create a dictionary matching each all-star indicator column to the player's team.
    """
    player_team = {
        "lebron_james_played": "LA LAKERS",
        "anthony_davis_played": "LA LAKERS",
        "stephen_curry_played": "GOLDEN STATE",
        "nikola_jokic_played": "DENVER",
        "kevin_durant_played": "PHOENIX",
        "devin_booker_played": "PHOENIX",
        "jayson_tatum_played": "BOSTON",
        "jaylen_brown_played": "BOSTON",
        "giannis_antetokounmpo_played": "MILWAUKEE",
        "damian_lillard_played": "MILWAUKEE",
        "luka_doncic_played": "DALLAS",
        "shai_gilgeous_alexander_played": "OKLAHOMA CITY",
        "anthony_edwards_played": "MINNESOTA",
        "jalen_brunson_played": "NEW YORK",
        "julius_randle_played": "NEW YORK",
        "joel_embiid_played": "PHILADELPHIA",
        "tyrese_maxey_played": "PHILADELPHIA",
        "tyrese_haliburton_played": "INDIANA",
        "bam_adebayo_played": "MIAMI",
        "paul_george_played": "LA CLIPPERS",
        "kawhi_leonard_played": "LA CLIPPERS",
        "paolo_banchero_played": "ORLANDO",
        "donovan_mitchell_played": "CLEVELAND",
        "trae_young_played": "ATLANTA",
        "scottie_barnes_played": "TORONTO",
        "karl_anthony_towns_played": "MINNESOTA"
    }

    return player_team


def clean_player_name(player_column):
    """
    Convert a player indicator column name into a readable player name.
    """
    player_name = player_column.replace("_played", "")
    player_name = player_name.replace("_", " ")
    player_name = player_name.title()

    return player_name


def check_player_columns(df, player_team):
    """
    Check whether all player indicator columns in the dictionary exist in the dataset.
    """
    missing_player_columns = []

    for player_col in player_team.keys():
        if player_col not in df.columns:
            missing_player_columns.append(player_col)

    if len(missing_player_columns) > 0:
        raise ValueError(
            f"These player indicator columns are missing: {missing_player_columns}"
        )


def summarize_team_specific_viewership(df, player_team):
    """
    For each player, compare viewership in that player's team games when he played
    versus when he missed the game.
    """
    check_required_columns(
        df,
        ["team_1_raw", "team_2_raw", "vwrs"],
        "Final dataset"
    )

    check_player_columns(df, player_team)

    results = []
    skipped_players = []

    for player_col, team in player_team.items():

        team_games = df[
            (df["team_1_raw"] == team) |
            (df["team_2_raw"] == team)
        ]

        played_games = team_games[team_games[player_col] == 1]
        missed_games = team_games[team_games[player_col] == 0]

        if len(played_games) > 0 and len(missed_games) > 0:
            avg_played = played_games["vwrs"].mean()
            avg_missed = missed_games["vwrs"].mean()

            results.append({
                "player": clean_player_name(player_col),
                "team": team,
                "team_games": len(team_games),
                "games_played": len(played_games),
                "games_missed": len(missed_games),
                "avg_viewership_when_played": avg_played,
                "avg_viewership_when_missed": avg_missed,
                "difference": avg_played - avg_missed
            })

        else:
            skipped_players.append(clean_player_name(player_col))

    team_comparison = pd.DataFrame(results)

    team_comparison = team_comparison.sort_values(
        "difference",
        ascending=False
    )

    print("\nTeam-specific player viewership diagnostics:")
    print(f"Players included in comparison: {team_comparison.shape[0]}")
    print(f"Players skipped because they had no played or missed games: {len(skipped_players)}")

    if len(skipped_players) > 0:
        print("Skipped players:")
        print(skipped_players)

    print("\nLargest positive differences:")
    print(team_comparison.head())

    return team_comparison


def save_data(df, output_path):
   
    df.to_csv(output_path, index=False)

    print(f"\nSaved team-specific player comparison to: {output_path}")


# Main script

def main():
    input_file = "data/qss20_finalds.csv"
    output_file = "data/team_specific_player_viewership.csv"

    final_df = load_data(input_file)

    player_team = get_player_team_dictionary()

    team_comparison = summarize_team_specific_viewership(
        df=final_df,
        player_team=player_team
    )

    save_data(team_comparison, output_file)


if __name__ == "__main__":
    main()

