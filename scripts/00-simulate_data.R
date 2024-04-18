#### Preamble ####
# Purpose: Simulates games played between players and summary statistics
# for each player.
# Author: Shuyang Qiu
# Date: 17 April 2024
# Contact: shuyang.qiu@mail.utoronto.ca
# License: MIT
# Pre-requisites: None


#### Workspace setup ####
library(tidyverse)

#### Simulate data ####
set.seed(111)

num_players <- 100
num_games <- 1000

# Simulate games played
games <- tibble(
  winner = sample(0:1, size = num_games, replace = TRUE),
  player1 = sample(0:num_players, size = num_games, replace = TRUE),
  player2 = sample(0:num_players, size = num_games, replace = TRUE)
)

# Simulate player stats
player_stats <- tibble(
  id = 1:100,
  kills = sample(1000:10000, size = num_players, replace = TRUE),
  deaths = sample(1000:10000, size = num_players, replace = TRUE)
)

#### Validate data ####
games$winner == 0 | games$winner == 1
games$player1 > 0 & games$player1 <= 100
games$player2 > 0 & games$player2 <= 100

player_stats$id > 0 & player_stats$id <= 100
player_stats$wins > 0
player_stats$loss > 0
player_stats$kills > 0
player_stats$deaths > 0
