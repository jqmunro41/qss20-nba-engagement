#!/usr/bin/env python
# coding: utf-8
"""
01_player_viewership_summary.py

Purpose:
    Summarize how NBA game viewership differs when each all-star player played
    compared to when that player did not play.

Input:
    data/qss20_finalds.csv
        Final game-level dataset with ratings, all-star indicators, and controls.

Output:
    data/player_viewership_differences.csv
        Player-level summary showing average viewership when each all-star played,
        average viewership when they did not play, and the difference.
"""

import pandas as pd


#FUnctions

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
    Check that required columns are present in a dataset.
    """
    missing_columns = []

    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        raise ValueError(
            f"{dataset_name} is missing these required columns: {missing_columns}"
        )


def get_star_columns(df):
    """
    Identify all all-star indicator columns.

    All-star columns are defined as columns ending with '_played'.
    """
    star_columns = []

    for col in df.columns:
        if col.endswith("_played"):
            star_columns.append(col)

    print("\nAll-star indicator diagnostics:")
    print(f"Number of all-star indicator columns found: {len(star_columns)}")

    if len(star_columns) == 0:
        raise ValueError("No all-star indicator columns ending in '_played' were found.")

    return star_columns


def clean_player_name(player_column):
    """
    Convert a player indicator column name into a readable player name.
    """
    player_name = player_column.replace("_played", "")
    player_name = player_name.replace("_", " ")
    player_name = player_name.title()

    return player_name


def summarize_player_viewership(df, star_columns):
    """
    Calculate average viewership when each all-star played and did not play.
    """
    check_required_columns(
        df,
        ["vwrs"],
        "Final dataset"
    )

    results = []

    for player_col in star_columns:
        played_games = df[df[player_col] == 1]
        not_played_games = df[df[player_col] == 0]

        avg_played = played_games["vwrs"].mean()
        avg_not_played = not_played_games["vwrs"].mean()
        difference = avg_played - avg_not_played

        results.append({
            "player": clean_player_name(player_col),
            "games_played": len(played_games),
            "games_not_played": len(not_played_games),
            "avg_viewership_when_played": avg_played,
            "avg_viewership_when_not_played": avg_not_played,
            "difference": difference
        })

    player_summary = pd.DataFrame(results)

    player_summary = player_summary.sort_values(
        "difference",
        ascending=False
    )

    print("\nPlayer viewership summary diagnostics:")
    print(f"Rows in player summary: {player_summary.shape[0]}")
    print("Largest positive differences:")
    print(player_summary.head())

    return player_summary


def save_data(df, output_path):
    """
    Save the player-level summary dataset.
    """
    df.to_csv(output_path, index=False)

    print(f"\nSaved player viewership summary to: {output_path}")


#Main scripts

def main():
    input_file = "data/qss20_finalds.csv"
    output_file = "data/player_viewership_differences.csv"

    final_df = load_data(input_file)

    star_columns = get_star_columns(final_df)

    player_summary = summarize_player_viewership(
        df=final_df,
        star_columns=star_columns
    )

    save_data(player_summary, output_file)


if __name__ == "__main__":
    main()
