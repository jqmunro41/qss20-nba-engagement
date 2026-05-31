#!/usr/bin/env python
# coding: utf-8

"""
03_player_and_matchup_regressions.py

Purpose:
    Estimate how all-star player appearances and selected opposing-star matchups
    are associated with national NBA game viewership.

Input:
    data/qss20_finalds.csv
        Final game-level dataset with viewership, player indicators, team valuation,
        and game-level controls.

Outputs:
    data/player_regression_results.csv
        Regression results for one player indicator at a time.

    data/matchup_regression_results.csv
        Regression results for selected opposing-star matchup indicators.

"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf


#Functions

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


def create_log_viewership(df):
    """
    Create log-transformed viewership outcome variable.
    """
    check_required_columns(
        df,
        ["vwrs"],
        "Final dataset"
    )

    df = df.copy()
    df["log_vwrs"] = np.log(df["vwrs"])

    print("\nOutcome variable diagnostics:")
    print("Created log_vwrs from vwrs")
    print(f"Missing log_vwrs values: {df['log_vwrs'].isna().sum()}")

    return df


def get_star_columns(df):
    """
    Identify all player indicator columns ending in '_played'.
    """
    star_columns = []

    for col in df.columns:
        if col.endswith("_played"):
            star_columns.append(col)

    print("\nPlayer indicator diagnostics:")
    print(f"Number of player indicator columns found: {len(star_columns)}")

    if len(star_columns) == 0:
        raise ValueError("No player indicator columns ending in '_played' were found.")

    return star_columns


def clean_player_name(player_column):
    """
    Convert player indicator column name into readable player name.
    """
    player_name = player_column.replace("_played", "")
    player_name = player_name.replace("_", " ")
    player_name = player_name.title()

    return player_name


def get_control_columns(df):
    """
    Define and check regression control variables.
    """
    control_columns = [
        "avg_net_rating",
        "spread",
        "holiday",
        "total"
    ]

    existing_controls = []

    for col in control_columns:
        if col in df.columns:
            existing_controls.append(col)

    print("\nControl variable diagnostics:")
    print(f"Controls included: {existing_controls}")

    missing_controls = []

    for col in control_columns:
        if col not in df.columns:
            missing_controls.append(col)

    if len(missing_controls) > 0:
        print(f"Controls not found and excluded: {missing_controls}")

    return existing_controls


def run_player_regressions(df, min_appearances):
    """
    Run one regression per player indicator column.

    Each model predicts log viewership using one player indicator and game-level
    controls. Robust HC3 standard errors are used.
    """
    check_required_columns(
        df,
        ["log_vwrs"],
        "Final dataset"
    )

    star_columns = get_star_columns(df)
    control_columns = get_control_columns(df)

    appearance_counts = df[star_columns].sum()
    star_columns_kept = appearance_counts[
        appearance_counts >= min_appearances
    ].index.tolist()

    print("\nPlayer regression diagnostics:")
    print(f"Minimum appearances required: {min_appearances}")
    print(f"Players included in regressions: {len(star_columns_kept)}")

    results = []

    for player_col in star_columns_kept:

        regression_columns = ["log_vwrs", player_col] + control_columns
        reg_df = df[regression_columns].dropna()

        x_vars = [player_col] + control_columns

        X = reg_df[x_vars]
        y = reg_df["log_vwrs"]

        X = sm.add_constant(X)

        model = sm.OLS(y, X).fit(cov_type="HC3")

        coef_log = model.params[player_col]
        percent_effect = (np.exp(coef_log) - 1) * 100

        results.append({
            "player": clean_player_name(player_col),
            "player_column": player_col,
            "appearances": int(appearance_counts[player_col]),
            "coef_log": coef_log,
            "percent_effect": percent_effect,
            "p_value": model.pvalues[player_col],
            "r_squared": model.rsquared,
            "n_obs": int(model.nobs)
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "coef_log",
        ascending=False
    )

    print("\nTop player regression results:")
    print(results_df.head())

    return results_df


def get_matchup_dictionary():
    """
    Define selected opposing-star matchups.

    Each matchup contains two player indicator columns.
    """
    matchups = {
        "lillard_brown": ("damian_lillard_played", "jaylen_brown_played"),
        "tatum_lillard": ("jayson_tatum_played", "damian_lillard_played"),
        "jokic_curry": ("nikola_jokic_played", "stephen_curry_played"),
        "lillard_brunson": ("damian_lillard_played", "jalen_brunson_played"),
        "giannis_brunson": ("giannis_antetokounmpo_played", "jalen_brunson_played"),
        "giannis_brown": ("giannis_antetokounmpo_played", "jaylen_brown_played"),
        "giannis_tatum": ("giannis_antetokounmpo_played", "jayson_tatum_played"),
        "brown_randle": ("jaylen_brown_played", "julius_randle_played"),
        "durant_doncic": ("kevin_durant_played", "luka_doncic_played"),
        "durant_jokic": ("kevin_durant_played", "nikola_jokic_played"),
        "doncic_booker": ("luka_doncic_played", "devin_booker_played"),
        "jokic_george": ("nikola_jokic_played", "paul_george_played")
    }

    return matchups


def check_matchup_columns(df, matchups):
    """
    Check that all player columns used in matchup regressions exist.
    """
    required_columns = []

    for matchup_name, players in matchups.items():
        player_1, player_2 = players
        required_columns.append(player_1)
        required_columns.append(player_2)

    required_columns = list(set(required_columns))

    check_required_columns(
        df,
        required_columns,
        "Final dataset"
    )


def create_matchup_indicators(df, matchups):
    """
    Create an indicator for each matchup.

    A matchup equals 1 when both players played in the same game.
    """
    df = df.copy()

    check_matchup_columns(df, matchups)

    for matchup_name, players in matchups.items():
        player_1, player_2 = players

        df[matchup_name] = (
            (df[player_1] == 1) &
            (df[player_2] == 1)
        ).astype(int)

    print("\nMatchup game counts:")

    for matchup_name in matchups:
        print(f"{matchup_name}: {int(df[matchup_name].sum())}")

    return df


def run_matchup_regressions(df, matchups):
    """
    Run one regression per matchup indicator.

    Each model predicts log viewership using one matchup indicator and game-level
    controls. Robust HC3 standard errors are used.
    """
    required_columns = [
        "log_vwrs",
        "avg_team_valuation_bil",
        "holiday",
        "spread",
        "total",
        "avg_net_rating"
    ]

    check_required_columns(
        df,
        required_columns,
        "Final dataset"
    )

    results = []

    for matchup_name, players in matchups.items():

        player_1, player_2 = players

        formula = (
            f"log_vwrs ~ {matchup_name} + "
            "avg_team_valuation_bil + holiday + spread + total + avg_net_rating"
        )

        model = smf.ols(
            formula=formula,
            data=df
        ).fit(cov_type="HC3")

        coef_log = model.params[matchup_name]
        percent_effect = (np.exp(coef_log) - 1) * 100

        results.append({
            "matchup": matchup_name,
            "player_1": clean_player_name(player_1),
            "player_2": clean_player_name(player_2),
            "games_together": int(df[matchup_name].sum()),
            "coef_log": coef_log,
            "percent_effect": percent_effect,
            "p_value": model.pvalues[matchup_name],
            "r_squared": model.rsquared,
            "n_obs": int(model.nobs)
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "coef_log",
        ascending=False
    )

    print("\nTop matchup regression results:")
    print(results_df.head())

    return results_df


def save_data(df, output_path):
    """
    Save a dataframe as a CSV file.
    """
    df.to_csv(output_path, index=False)

    print(f"\nSaved file to: {output_path}")

#Main script

def main():
    input_file = "data/qss20_finalds.csv"
    player_output_file = "data/player_regression_results.csv"
    matchup_output_file = "data/matchup_regression_results.csv"

    df = load_data(input_file)
    df = create_log_viewership(df)

    player_results = run_player_regressions(
        df=df,
        min_appearances=10
    )

    matchups = get_matchup_dictionary()

    df = create_matchup_indicators(
        df=df,
        matchups=matchups
    )

    matchup_results = run_matchup_regressions(
        df=df,
        matchups=matchups
    )

    save_data(
        df=player_results,
        output_path=player_output_file
    )

    save_data(
        df=matchup_results,
        output_path=matchup_output_file
    )


if __name__ == "__main__":
    main()
