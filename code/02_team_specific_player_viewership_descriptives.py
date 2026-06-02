#!/usr/bin/env python
# coding: utf-8

"""
02_team_specific_player_viewership_descriptives.py

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
    Create a dictionary matching each all-star indicator column to the player's
    full team name. These names should match team_1_full and team_2_full.
    """
    player_team = {
        "lebron_james_played": "Los Angeles Lakers",
        "anthony_davis_played": "Los Angeles Lakers",
        "stephen_curry_played": "Golden State Warriors",
        "nikola_jokic_played": "Denver Nuggets",
        "kevin_durant_played": "Phoenix Suns",
        "devin_booker_played": "Phoenix Suns",
        "jayson_tatum_played": "Boston Celtics",
        "jaylen_brown_played": "Boston Celtics",
        "giannis_antetokounmpo_played": "Milwaukee Bucks",
        "damian_lillard_played": "Milwaukee Bucks",
        "luka_doncic_played": "Dallas Mavericks",
        "shai_gilgeous_alexander_played": "Oklahoma City Thunder",
        "anthony_edwards_played": "Minnesota Timberwolves",
        "jalen_brunson_played": "New York Knicks",
        "julius_randle_played": "New York Knicks",
        "joel_embiid_played": "Philadelphia 76ers",
        "tyrese_maxey_played": "Philadelphia 76ers",
        "tyrese_haliburton_played": "Indiana Pacers",
        "bam_adebayo_played": "Miami Heat",
        "paul_george_played": "Los Angeles Clippers",
        "kawhi_leonard_played": "Los Angeles Clippers",
        "paolo_banchero_played": "Orlando Magic",
        "donovan_mitchell_played": "Cleveland Cavaliers",
        "trae_young_played": "Atlanta Hawks",
        "scottie_barnes_played": "Toronto Raptors",
        "karl_anthony_towns_played": "Minnesota Timberwolves"
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


def prepare_team_names(df):
    """
    Clean team_1_full and team_2_full so matching is consistent.
    """
    df = df.copy()

    df["team_1_full_clean"] = df["team_1_full"].astype(str).str.strip().str.upper()
    df["team_2_full_clean"] = df["team_2_full"].astype(str).str.strip().str.upper()

    return df


def summarize_team_specific_viewership(df, player_team):
    """
    For each player, compare viewership in that player's team games when he played
    versus when he missed the game.

    This version uses team_1_full and team_2_full so it counts all games involving
    the player's team.
    """
    check_required_columns(
        df,
        ["team_1_full", "team_2_full", "vwrs"],
        "Final dataset"
    )

    check_player_columns(df, player_team)

    df = prepare_team_names(df)

    results = []
    skipped_players = []

    for player_col, team in player_team.items():

        team_clean = team.strip().upper()

        team_games = df[
            (df["team_1_full_clean"] == team_clean) |
            (df["team_2_full_clean"] == team_clean)
        ].copy()

        # Convert player indicator to numeric.
        # Missing values are treated as 0 within that player's team games.
        team_games[player_col] = pd.to_numeric(
            team_games[player_col],
            errors="coerce"
        ).fillna(0)

        played_games = team_games[team_games[player_col] == 1]
        missed_games = team_games[team_games[player_col] == 0]

        if len(team_games) == 0:
            skipped_players.append(clean_player_name(player_col))
            continue

        if len(played_games) > 0 and len(missed_games) > 0:
            avg_played = played_games["vwrs"].mean()
            avg_missed = missed_games["vwrs"].mean()
            difference = avg_played - avg_missed
        elif len(played_games) > 0 and len(missed_games) == 0:
            avg_played = played_games["vwrs"].mean()
            avg_missed = None
            difference = None
        elif len(played_games) == 0 and len(missed_games) > 0:
            avg_played = None
            avg_missed = missed_games["vwrs"].mean()
            difference = None
        else:
            avg_played = None
            avg_missed = None
            difference = None

        results.append({
            "player": clean_player_name(player_col),
            "team": team,
            "team_games": len(team_games),
            "games_played": len(played_games),
            "games_missed": len(missed_games),
            "avg_viewership_when_played": avg_played,
            "avg_viewership_when_missed": avg_missed,
            "difference": difference
        })

    team_comparison = pd.DataFrame(results)

    team_comparison = team_comparison.sort_values(
        "difference",
        ascending=False,
        na_position="last"
    )

    print("\nTeam-specific player viewership diagnostics:")
    print(f"Players included in output: {team_comparison.shape[0]}")
    print(f"Players skipped because their team had no games: {len(skipped_players)}")

    if len(skipped_players) > 0:
        print("Skipped players:")
        print(skipped_players)

    print("\nLargest positive differences:")
    print(team_comparison.head())

    return team_comparison


def save_data(df, output_path):
    """
    Save output dataset.
    """
    df.to_csv(output_path, index=False)

    print(f"\nSaved team-specific player comparison to: {output_path}")


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
