#### Preamble ####
# Purpose: Generates model for win percentage base on various summary statistics.
# Author: Shuyang Qiu
# Date: 17 April 2024
# Contact: shuyang.qiu@mail.utoronto.ca
# License: MIT
# Pre-requisites: None


#### Workspace setup ####
library(arrow)
library(rstanarm)


data <- read_parquet("./data/analysis_data/analysis_data.parquet")
seed <- 111

### Model data ####
winrates <-
  stan_glm(
    win_percent ~ kill_death_ratio + hs + adr + rounds,
    data = data,
    family = binomial(link = "logit"),
    weights = games_played,
    seed = seed
  )


#### Save model ####
saveRDS(
  winrates,
  file = "./models/winrates.rds"
)