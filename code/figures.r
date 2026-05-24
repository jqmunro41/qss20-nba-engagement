library(tidyverse)
library(readr)
library(dplyr)
library(lubridate)
library(fixest)
library(ggplot2)
library(ggthemes)
library(scales)

### NOTE: Added the small texts on the figures manually in PDF editor

df1 <- read_csv("Replication_files/Final_datasets/ratings_final.csv")

df2 <- read_csv("Replication_files/Final_datasets/nba_highlights_final.csv")

## Figure 1 in Paper (plots NBA viewership and percent of field goal attempts from three over time)

# ---- Paths ----
path_view  <- "Replication_files/Data/nba_viewership_2009_2025.csv"
path_nba   <- "Replication_files/Data/full_NBA_data.csv"

# ---- Read viewership (already season-level) ----
view_df <- read.csv(path_view, check.names = FALSE) %>%
  as_tibble() %>%
  rename(season = year, viewership_millions = viewership_millions) %>%
  mutate(season = as.character(season))

# ---- Read NBA stats and compute league averages by season ----
nba_raw <- read.csv(path_nba, check.names = FALSE) %>% as_tibble()

nba_season <- nba_raw %>%
  mutate(season = as.character(SEASON)) %>%
  group_by(season) %>%
  summarise(
    pct_fga_from_three = mean(AVG_PCT_FGA_3PT, na.rm = TRUE),
    pace               = mean(AVG_PACE,               na.rm = TRUE),
    .groups = "drop"
  )

# ---- Join viewership to season averages ----
df <- view_df %>%
  inner_join(nba_season, by = "season") %>%
  arrange(season)

base_season <- "2009-10"  # index baseline
df_idx <- df %>%
  mutate(
    viewership_index       = 100 * viewership_millions / viewership_millions[season == base_season],
    pct_fga_from_three_idx = 100 * pct_fga_from_three / pct_fga_from_three[season == base_season],
  )

plot_df <- df_idx %>%
  select(season, viewership_index, pct_fga_from_three_idx) %>%
  pivot_longer(-season, names_to = "metric", values_to = "index") %>%
  mutate(
    season = factor(season, levels = df$season),
    metric = recode(metric,
                    viewership_index       = "Viewership",
                    pct_fga_from_three_idx = "% FGA from 3")
  )


# ---- Plot ----
ggplot(plot_df, aes(season, index, group = metric, color = metric)) +
  geom_line(linewidth = 1.1) +
  labs(
    title = "NBA: Viewership vs. Threes Attempted (2009-2025)",
    x = "Season",
    color = NULL,
    y = NULL,
  ) +
  scale_color_manual(values = c(
    "% FGA from 3" = "#1b9e77",   # green tone
    "Viewership"     = "red")) +
  scale_y_continuous(labels = NULL) +
  theme_few() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    axis.ticks.y = element_blank(),  # removes y-axis tick marks
    axis.text.y = element_blank(),   # removes y-axis numbers
    legend.position = "bottom"
  )



## Figure 2 in Paper (log(VWRs) vs % Points From Threes)
ggplot(df1, aes(x = pct_points_from_3pt, y = log(vwrs), color = network)) +
  geom_point(alpha = 0.75, size = 2.2) +
  geom_smooth(aes(color = NULL), method = "lm", se = TRUE, linewidth = 1) +
  scale_x_continuous(labels = percent_format(accuracy = 1),
                     name = "Percent of Points from 3PT") +
  labs(
    y = "log(VWRs)",
    title = "log(VWRs) vs. Percent of Points from 3",
    #subtitle = paste0("One OLS line across all networks • N = ", nrow(plot_df)),
    color = "network",
    #caption = eq_label
  ) +
  theme_few(base_size = 12) + 
  theme(legend.position = "bottom")

## Figure 5 in Paper (log(VWRs) vs % Points From FTs)
ggplot(df1, aes(x = PCT_PTS_FT_GAME, y = log(vwrs), color = network)) +
  geom_point(alpha = 0.75, size = 2.2) +
  geom_smooth(aes(color = NULL), method = "lm", se = TRUE, linewidth = 1) +
  scale_x_continuous(labels = percent_format(accuracy = 1),
                     name = "Percent of Points from FTs") +
  labs(
    y = "log(VWRs)",
    title = "log(VWRs) vs. % of Points from FTs",
    #subtitle = paste0("One OLS line across all networks • N = ", nrow(plot_df)),
    color = "network",
    #caption = eq_label
  ) +
  theme_few(base_size = 12) + 
  theme(legend.position = "none")

## Figure 6 in paper (Games missed by all-stars each season)

# ---- Load data ----
df3 <- read.csv("Replication_files/Data/total_games_missed_by_season.csv")

df3$season_label <- recode(df3$season,
                           "1516" = "2015-16",
                           "1617" = "2016-17",
                           "1718" = "2017-18",
                           "1819" = "2018-19",
                           "1920" = "2019-20",
                           "2021" = "2020-21",
                           "2122" = "2021-22",
                           "2223" = "2022-23",
                           "2324" = "2023-24",
                           "2425" = "2024-25"
)

# Make sure ggplot keeps the order
df3$season_label <- factor(df3$season_label, levels = df3$season_label)

# ---- Plot ----
ggplot(df3, aes(x = season_label, y = total_games_missed, group = 1)) +
  geom_line(size = 1.2, color = "green") +
  geom_point(size = 3, color = "green") +
  theme_minimal(base_size = 14) +
  labs(
    title = "Total Games Missed by All-Stars per Season",
    x = "Season",
    y = "Total Games Missed"
  ) +
  theme_few()

