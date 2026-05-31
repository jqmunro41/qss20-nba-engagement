#!/usr/bin/env python
# coding: utf-8

"""
04_prediction_lift_by_player.py

Purpose:
    Use a random forest model to predict NBA national TV viewership and estimate
    each player's prediction lift using cross-validated predictions.

    Prediction lift is calculated as:
        average predicted viewership when a player played
        minus
        average predicted viewership when that player did not play.

Input:
    data/qss20_finalds.csv
        Final game-level dataset with viewership, player indicators, and controls.

Outputs:
    data/prediction_lift_model_evaluation.csv
        Cross-validated model evaluation metrics, including R-squared, MAE, RMSE,
        and comparison to a baseline model that predicts average viewership.

    data/prediction_lift_by_player.csv
        Player-level prediction lift results using cross-validated predictions.

    output/prediction_lift_by_player.png
        Bar chart of the top 15 players by predicted viewership lift.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_predict
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


#Functions

def make_output_folders():
    """
    Create data and output folders if they do not already exist.
    """
    os.makedirs("data", exist_ok=True)
    os.makedirs("output", exist_ok=True)

    print("\nChecked output folders:")
    print("data/")
    print("output/")


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


def get_star_columns(df, min_appearances):
    """
    Identify player indicator columns and keep only players with enough appearances.
    """
    star_columns = []

    for col in df.columns:
        if col.endswith("_played"):
            star_columns.append(col)

    if len(star_columns) == 0:
        raise ValueError("No player indicator columns ending in '_played' were found.")

    appearance_counts = df[star_columns].sum()

    star_columns_kept = appearance_counts[
        appearance_counts >= min_appearances
    ].index.tolist()

    print("\nPlayer indicator diagnostics:")
    print(f"Total player indicator columns found: {len(star_columns)}")
    print(f"Minimum appearances required: {min_appearances}")
    print(f"Player indicator columns kept: {len(star_columns_kept)}")

    if len(star_columns_kept) == 0:
        raise ValueError("No players met the minimum appearance cutoff.")

    return star_columns_kept, appearance_counts


def get_control_columns(df):
    """
    Define and keep available game-level control variables.
    """
    possible_controls = [
        "avg_net_rating",
        "spread",
        "holiday",
        "total"
    ]

    control_columns = []

    for col in possible_controls:
        if col in df.columns:
            control_columns.append(col)

    print("\nControl variable diagnostics:")
    print(f"Controls included: {control_columns}")

    missing_controls = []

    for col in possible_controls:
        if col not in df.columns:
            missing_controls.append(col)

    if len(missing_controls) > 0:
        print(f"Controls not found and excluded: {missing_controls}")

    if len(control_columns) == 0:
        raise ValueError("No control columns were found.")

    return control_columns


def prepare_model_data(df, outcome_column, predictor_columns):
    """
    Keep outcome and predictor columns, then drop rows with missing values.
    """
    check_required_columns(
        df,
        [outcome_column] + predictor_columns,
        "Final dataset"
    )

    model_df = df[
        [outcome_column] + predictor_columns
    ].dropna()

    print("\nModel data diagnostics:")
    print(f"Rows before dropping missing values: {df.shape[0]}")
    print(f"Rows after dropping missing values: {model_df.shape[0]}")
    print(f"Number of predictors: {len(predictor_columns)}")

    X = model_df[predictor_columns]
    y = model_df[outcome_column]

    return X, y


def fit_random_forest():
    """
    Define the random forest regression model.
    """
    rf_model = RandomForestRegressor(
        n_estimators=500,
        random_state=1
    )

    return rf_model


def get_cross_validated_predictions(model, X, y, n_splits):
    """
    Generate out-of-sample predictions for every row using K-fold cross-validation.
    """
    cv = KFold(
        n_splits=n_splits,
        shuffle=True,
        random_state=1
    )

    y_pred = cross_val_predict(
        model,
        X,
        y,
        cv=cv
    )

    print("\nCross-validation diagnostics:")
    print(f"Number of folds: {n_splits}")
    print(f"Rows receiving out-of-sample predictions: {len(y_pred)}")

    return y_pred


def evaluate_model(y, y_pred):
    """
    Evaluate cross-validated model predictions and compare to a baseline model.

    The baseline model always predicts average viewership.
    """
    model_r2 = r2_score(y, y_pred)
    model_mae = mean_absolute_error(y, y_pred)
    model_rmse = mean_squared_error(y, y_pred) ** 0.5

    baseline_pred = [y.mean()] * len(y)

    baseline_mae = mean_absolute_error(y, baseline_pred)
    baseline_rmse = mean_squared_error(y, baseline_pred) ** 0.5

    mae_improvement = baseline_mae - model_mae
    rmse_improvement = baseline_rmse - model_rmse

    evaluation_df = pd.DataFrame({
        "metric": [
            "cross_validated_r_squared",
            "cross_validated_mae",
            "cross_validated_rmse",
            "baseline_mae",
            "baseline_rmse",
            "mae_improvement_over_baseline",
            "rmse_improvement_over_baseline",
            "n_obs"
        ],
        "value": [
            model_r2,
            model_mae,
            model_rmse,
            baseline_mae,
            baseline_rmse,
            mae_improvement,
            rmse_improvement,
            len(y)
        ]
    })

    print("\nModel evaluation:")
    print(evaluation_df)

    return evaluation_df


def clean_player_name(player_column):
    """
    Convert player indicator column name into a readable player name.
    """
    player_name = player_column.replace("_played", "")
    player_name = player_name.replace("_", " ")
    player_name = player_name.title()

    return player_name


def calculate_prediction_lift(X, y, y_pred, star_columns, appearance_counts):
    """
    Calculate player-level prediction lift using cross-validated predictions.

    Prediction lift equals:
        average predicted viewership when player played
        minus
        average predicted viewership when player did not play.
    """
    prediction_results = X.copy()
    prediction_results["actual_vwrs"] = y
    prediction_results["predicted_vwrs"] = y_pred

    lift_results = []

    for player_col in star_columns:

        played_pred = prediction_results.loc[
            prediction_results[player_col] == 1,
            "predicted_vwrs"
        ]

        not_played_pred = prediction_results.loc[
            prediction_results[player_col] == 0,
            "predicted_vwrs"
        ]

        played_actual = prediction_results.loc[
            prediction_results[player_col] == 1,
            "actual_vwrs"
        ]

        not_played_actual = prediction_results.loc[
            prediction_results[player_col] == 0,
            "actual_vwrs"
        ]

        if len(played_pred) > 0 and len(not_played_pred) > 0:

            prediction_lift = played_pred.mean() - not_played_pred.mean()
            actual_difference = played_actual.mean() - not_played_actual.mean()

            lift_results.append({
                "player": clean_player_name(player_col),
                "player_column": player_col,
                "total_appearances": int(appearance_counts[player_col]),
                "prediction_sample_appearances": int(prediction_results[player_col].sum()),
                "avg_predicted_when_played": played_pred.mean(),
                "avg_predicted_when_not_played": not_played_pred.mean(),
                "prediction_lift": prediction_lift,
                "avg_actual_when_played": played_actual.mean(),
                "avg_actual_when_not_played": not_played_actual.mean(),
                "actual_difference": actual_difference
            })

    lift_df = pd.DataFrame(lift_results)

    lift_df = lift_df.sort_values(
        "prediction_lift",
        ascending=False
    )

    print("\nPrediction lift results:")
    print(lift_df)

    return lift_df


def save_data(df, output_path):
    """
    Save a dataframe as a CSV file.
    """
    df.to_csv(output_path, index=False)

    print(f"\nSaved file to: {output_path}")


def plot_prediction_lift(lift_df, output_path, top_n):
    """
    Save a horizontal bar chart of the top players by prediction lift.
    """
    top_players = lift_df.head(top_n).sort_values(
        "prediction_lift",
        ascending=True
    )

    plt.figure(figsize=(10, 7))

    plt.barh(
        top_players["player"],
        top_players["prediction_lift"]
    )

    plt.xlabel("Difference in Predicted Viewership")
    plt.ylabel("Player")
    plt.title("Predicted Viewership Lift by Player")

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"\nSaved prediction lift figure to: {output_path}")


# Main script

def main():
    input_file = "data/qss20_finalds.csv"

    evaluation_output_file = "data/prediction_lift_model_evaluation.csv"
    lift_output_file = "data/prediction_lift_by_player.csv"
    figure_output_file = "output/prediction_lift_by_player.png"

    outcome_column = "vwrs"
    min_appearances = 10
    top_n_players = 15
    n_splits = 5

    make_output_folders()

    df = load_data(input_file)

    star_columns, appearance_counts = get_star_columns(
        df=df,
        min_appearances=min_appearances
    )

    control_columns = get_control_columns(df)

    predictor_columns = star_columns + control_columns

    X, y = prepare_model_data(
        df=df,
        outcome_column=outcome_column,
        predictor_columns=predictor_columns
    )

    rf_model = fit_random_forest()

    y_pred = get_cross_validated_predictions(
        model=rf_model,
        X=X,
        y=y,
        n_splits=n_splits
    )

    evaluation_df = evaluate_model(
        y=y,
        y_pred=y_pred
    )

    lift_df = calculate_prediction_lift(
        X=X,
        y=y,
        y_pred=y_pred,
        star_columns=star_columns,
        appearance_counts=appearance_counts
    )

    save_data(
        df=evaluation_df,
        output_path=evaluation_output_file
    )

    save_data(
        df=lift_df,
        output_path=lift_output_file
    )

    plot_prediction_lift(
        lift_df=lift_df,
        output_path=figure_output_file,
        top_n=top_n_players
    )


if __name__ == "__main__":
    main()
