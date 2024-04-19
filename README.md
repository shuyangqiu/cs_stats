# Predicting Counter-Strike Win Rates Using Player Statistics

## Overview

Counter-Strike player statistics were used to create a model to predict their team's win rate. Predictors used include player performance metrics such as
average damage per round and overall statistics such as total number of rounds played.


## File Structure

The repo is structured as:

-   `data/raw_data` contains the raw data as obtained from HLTV.org.
-   `data/analysis_data` contains the cleaned dataset that was constructed.
-   `models` contains the fitted model and an API for the model. 
-   `other` contains relevant literature, details about LLM chat interactions, and sketches.
-   `paper` contains the files used to generate the paper, including the Quarto document and reference bibliography file, as well as the PDF of the paper. 
-   `scripts` contains the Python and R scripts used to simulate, download and clean data.

## API
A Python Flask API has been provided in the `models` folder. The API can be hosted using
```
flask --app .\model_api.py run
```
### POST /predict
Endpoint returns the predicted win rate with given parameters.

Example request body
```
{
  kdr: 1,
  hs: 60,
  adr: 70,
  rounds: 10000
}
```
Example response
```
{0.494517259191938}
```

## Statement on LLM usage

No LLMs were used to produce this paper.
