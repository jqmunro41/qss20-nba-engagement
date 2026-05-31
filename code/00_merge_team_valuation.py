#!/usr/bin/env python
# coding: utf-8

# In[3]:


"""
00_merge_team_valuation.py

Purpose:
    Merge the game-level average team valuation variable into the ratings/all-star
    dataset.

Inputs:
    data/ratings_final_allstar_indicators.csv
        Main game-level dataset with ratings, all-star indicators, and controls.

    data/team_valuation_game_level.csv
        Game-level dataset containing GAME_ID and avg_team_valuation_bil.

Output:
    data/qss20_finalds.csv
        Final merged dataset with avg_team_valuation_bil included.
"""

import pandas as pd


#FUnctions

def load_data(file_path):
    """
    Load a CSV file and print basic information about it.
    """
    df = pd.read_csv(file_path)

    print(f"\nLoaded file: {file_path}")
    print(f"Rows: {df.shape[0]}")
    print(f"Columns: {df.shape[1]}")

    return df


def check_required_columns(df, required_columns, dataset_name):
    """
    Check that the required columns are present in a dataset.
    """
    missing_columns = []

    for col in required_columns:
        if col not in df.columns:
            missing_columns.append(col)

    if len(missing_columns) > 0:
        raise ValueError(
            f"{dataset_name} is missing these required columns: {missing_columns}"
        )


def prepare_valuation_data(valuation_df):
    """
    Keep only GAME_ID and avg_team_valuation_bil, then remove duplicate GAME_IDs.
    """
    check_required_columns(
        valuation_df,
        ["GAME_ID", "avg_team_valuation_bil"],
        "Team valuation dataset"
    )

    valuation_clean = valuation_df[
        ["GAME_ID", "avg_team_valuation_bil"]
    ].copy()

    duplicate_games = valuation_clean["GAME_ID"].duplicated().sum()

    print("\nTeam valuation data diagnostics:")
    print(f"Duplicate GAME_ID rows before cleaning: {duplicate_games}")

    valuation_clean = valuation_clean.drop_duplicates(subset="GAME_ID")

    print(f"Rows after dropping duplicate GAME_IDs: {valuation_clean.shape[0]}")

    return valuation_clean


def merge_team_valuation(final_df, valuation_df):
    """
    Merge avg_team_valuation_bil into the final ratings/all-star dataset.
    """
    check_required_columns(
        final_df,
        ["GAME_ID"],
        "Ratings/all-star dataset"
    )

    check_required_columns(
        valuation_df,
        ["GAME_ID", "avg_team_valuation_bil"],
        "Cleaned team valuation dataset"
    )

    print("\nPre-merge diagnostics:")
    print(f"Rows in ratings/all-star dataset: {final_df.shape[0]}")
    print(f"Rows in team valuation dataset: {valuation_df.shape[0]}")
    print(f"Unique GAME_IDs in ratings/all-star dataset: {final_df['GAME_ID'].nunique()}")
    print(f"Unique GAME_IDs in team valuation dataset: {valuation_df['GAME_ID'].nunique()}")

    merged_df = final_df.merge(
        valuation_df,
        on="GAME_ID",
        how="left"
    )

    print("\nPost-merge diagnostics:")
    print(f"Rows in merged dataset: {merged_df.shape[0]}")
    print(f"Columns in merged dataset: {merged_df.shape[1]}")
    print(
        "Missing avg_team_valuation_bil values:",
        merged_df["avg_team_valuation_bil"].isna().sum()
    )

    if merged_df.shape[0] != final_df.shape[0]:
        raise ValueError(
            "The number of rows changed during the merge. Check for duplicate GAME_IDs."
        )

    return merged_df


def save_data(df, output_path):
    """
    Save a dataframe as a CSV.
    """
    df.to_csv(output_path, index=False)

    print(f"\nSaved merged dataset to: {output_path}")


# Main script

def main():
    ratings_file = "data/ratings_final_allstar_indicators.csv"
    valuation_file = "data/team_valuation_game_level.csv"
    output_file = "data/qss20_finalds.csv"

    ratings_df = load_data(ratings_file)
    valuation_df = load_data(valuation_file)

    valuation_clean = prepare_valuation_data(valuation_df)

    merged_df = merge_team_valuation(
        final_df=ratings_df,
        valuation_df=valuation_clean
    )

    save_data(merged_df, output_file)


if __name__ == "__main__":
    main()

