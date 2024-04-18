#### Preamble ####
# Purpose: Tests cleaned player data.
# Author: Shuyang Qiu
# Date: 17 April 2024
# Contact: shuyang.qiu@mail.utoronto.ca
# License: MIT
# Pre-requisites: None


#### Workspace setup ####
library(tidyverse)
library(arrow)

#### Test data ####
data <- read_parquet("./data/analysis_data/analysis_data.parquet")

# Check column data types
class(data$id) == "character"
class(data$name) == "character"
class(data$win) == "numeric"
class(data$loss) == "numeric"
class(data$kills) == "numeric"
class(data$deaths) == "numeric"
class(data$hs) == "numeric"
class(data$adr) == "numeric"
class(data$rounds) == "numeric"
class(data$games_played) == "numeric"
class(data$win_percent) == "numeric"
class(data$kill_death_ratio) == "numeric"

# Check column values are valid
all(data$win >= 0)
all(data$loss >= 0)
all(data$kills >= 0)
all(data$deaths >= 0)
all(data$hs >= 0 & data$hs <= 100)
all(data$adr >= 0)
all(data$rounds >= 0)
all(data$games_played == data$win + data$loss)
all(data$win_percent == data$win / data$games_played)
all(data$kill_death_ratio == data$kills / data$deaths)

# Check number of wins is equal to number of losses
data$win |> sum() == data$loss |> sum()