#### Preamble ####
# Purpose: Cleans and adds additional features to data.
# Author: Shuyang Qiu
# Date: 17 April 2024
# Contact: shuyang.qiu@mail.utoronto.ca
# License: MIT
# Pre-requisites: None

#### Workspace setup ####
library(tidyverse)
library(arrow)

#### Clean data ####
# Read data
raw_data <-
  read_csv(
    "./data/raw_data/raw_data.csv",
    col_names = c("name", "win", "loss", "kills", "deaths", "hs", "adr", "rounds")
  )

# Clean data
cleaned_data <-
  raw_data |> 
  separate("name", into = c("id", "name"), sep = "/") |> # Split name column
  mutate(hs = as.numeric(gsub("%", "", hs))) # Remove % sign from headshot column

# Add additional columns
cleaned_data$games_played <- cleaned_data$win + cleaned_data$loss
cleaned_data$win_percent <- cleaned_data$win / cleaned_data$games_played
cleaned_data$kill_death_ratio <- cleaned_data$kills / cleaned_data$deaths

#### Save data ####
write_parquet(cleaned_data, "./data/analysis_data/analysis_data.parquet")