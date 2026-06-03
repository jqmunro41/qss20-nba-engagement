"""
05_make_lightning_talk_figures.py

Purpose:
    Create presentation-ready figures for the final lightning talk using
    player-level and team-specific viewership difference datasets.

Inputs:
    data/player_viewership_differences.csv
    data/team_specific_player_viewership.csv

Outputs:
    output/figures/fig1_top_player_viewership_lift.png
    output/figures/fig2_team_specific_viewership_lift.png
    output/figures/fig3_played_vs_missed_viewership.png
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# --------------------------------------------------
# File paths
# --------------------------------------------------

PLAYER_VIEWERSHIP_PATH = "data/player_viewership_differences.csv"
TEAM_VIEWERSHIP_PATH = "data/team_specific_player_viewership.csv"
FIGURE_DIR = "output"


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def create_output_folder(folder_path):
    """
    Create output folder if it does not already exist.
    """
    os.makedirs(folder_path, exist_ok=True)


def load_data(player_path, team_path):
    """
    Load player-level and team-specific viewership datasets.

    Parameters
    ----------
    player_path : str
        Path to player-level viewership difference dataset.

    team_path : str
        Path to team-specific player viewership dataset.

    Returns
    -------
    player_df : pandas DataFrame
        Dataset comparing average viewership when each player played vs. did not play.

    team_df : pandas DataFrame
        Dataset comparing average viewership when each player played vs. missed games
        specifically for that player's team.
    """
    player_df = pd.read_csv(player_path)
    team_df = pd.read_csv(team_path)

    print("Loaded player-level viewership data:")
    print(f"Rows: {len(player_df)}")
    print(f"Columns: {list(player_df.columns)}")

    print("\nLoaded team-specific viewership data:")
    print(f"Rows: {len(team_df)}")
    print(f"Columns: {list(team_df.columns)}")

    return player_df, team_df


def save_figure(file_name):
    """
    Save the current matplotlib figure to the output figure folder.
    """
    output_path = os.path.join(FIGURE_DIR, file_name)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Saved figure: {output_path}")
    plt.show()


def clean_player_names(df):
    """
    Clean player names for display.

    This keeps the analysis data the same, but makes graph labels
    look cleaner in presentation slides.
    """
    df = df.copy()

    df["player"] = (
        df["player"]
        .str.replace("_", " ", regex=False)
        .str.title()
    )

    return df


def plot_horizontal_bar(
    df,
    label_col,
    value_col,
    title,
    x_label,
    output_file,
    top_n=10
):
    """
    Make a horizontal bar chart for the top N values.

    Parameters
    ----------
    df : pandas DataFrame
        Data to plot.

    label_col : str
        Column used for y-axis labels.

    value_col : str
        Column used for bar length.

    title : str
        Plot title.

    x_label : str
        X-axis label.

    output_file : str
        Name of saved output file.

    top_n : int
        Number of rows to show.
    """
    plot_df = (
        df
        .sort_values(value_col, ascending=False)
        .head(top_n)
        .sort_values(value_col, ascending=True)
        .copy()
    )

    plt.figure(figsize=(9, 6))
    plt.barh(plot_df[label_col], plot_df[value_col])

    plt.title(title, fontsize=15, weight="bold")
    plt.xlabel(x_label)
    plt.ylabel("")

    for i, value in enumerate(plot_df[value_col]):
        plt.text(
            value,
            i,
            f" +{value:.0f}",
            va="center",
            fontsize=10
        )

    save_figure(output_file)


def plot_played_vs_missed(
    df,
    output_file,
    top_n=8
):
    """
    Make a dot-and-line plot comparing average viewership when a player
    played versus when that same player missed games.

    This is useful for the lightning talk because it directly shows the
    viewership gap.
    """
    plot_df = (
        df
        .sort_values("difference", ascending=False)
        .head(top_n)
        .sort_values("difference", ascending=True)
        .copy()
    )

    plot_df["player_team_label"] = (
        plot_df["player"] + " (" + plot_df["team"].str.title() + ")"
    )

    y_position = np.arange(len(plot_df))

    plt.figure(figsize=(9, 6))

    plt.scatter(
        plot_df["avg_viewership_when_missed"],
        y_position,
        label="When player missed",
        s=70
    )

    plt.scatter(
        plot_df["avg_viewership_when_played"],
        y_position,
        label="When player played",
        s=70
    )

    for i in range(len(plot_df)):
        plt.plot(
            [
                plot_df["avg_viewership_when_missed"].iloc[i],
                plot_df["avg_viewership_when_played"].iloc[i]
            ],
            [i, i],
            linewidth=2
        )

    plt.yticks(y_position, plot_df["player_team_label"])

    plt.title(
        "Average Viewership Was Higher When Certain Stars Played",
        fontsize=15,
        weight="bold"
    )
    plt.xlabel("Average Viewership, in Thousands")
    plt.ylabel("")
    plt.legend()

    save_figure(output_file)


# --------------------------------------------------
# Main analysis
# --------------------------------------------------

def main():
    """
    Run full figure-making script.
    """
    create_output_folder(FIGURE_DIR)

    player_df, team_df = load_data(
        PLAYER_VIEWERSHIP_PATH,
        TEAM_VIEWERSHIP_PATH
    )

    player_df = clean_player_names(player_df)
    team_df = clean_player_names(team_df)

    # Diagnostic checks for sample size
    print("\nPlayer-level sample size summary:")
    print(player_df[["games_played", "games_not_played"]].describe())

    print("\nTeam-specific sample size summary:")
    print(team_df[["team_games", "games_played", "games_missed"]].describe())

    # Figure 1: overall player viewership lift
    plot_horizontal_bar(
        df=player_df,
        label_col="player",
        value_col="difference",
        title="Players Associated with the Largest National Viewership Increase",
        x_label="Average Viewership Increase When Player Played, in Thousands",
        output_file="fig1_top_player_viewership_lift.png",
        top_n=10
    )

    # Figure 2: team-specific player viewership lift
    team_df["player_team_label"] = (
        team_df["player"] + " (" + team_df["team"].str.title() + ")"
    )

    plot_horizontal_bar(
        df=team_df,
        label_col="player_team_label",
        value_col="difference",
        title="Largest Team-Specific Viewership Increases",
        x_label="Average Viewership Increase When Player Played, in Thousands",
        output_file="fig2_team_specific_viewership_lift.png",
        top_n=10
    )

    # Figure 3: direct played vs. missed comparison
    plot_played_vs_missed(
        df=team_df,
        output_file="fig3_played_vs_missed_viewership.png",
        top_n=8
    )


if __name__ == "__main__":
    main()
