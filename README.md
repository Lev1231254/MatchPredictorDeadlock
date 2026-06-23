# Deadlock Match Predictor

## Description

An end-to-end machine learning pipeline that predicts match outcomes for the game *Deadlock*.
This project covers the full data lifecycle: fetching raw match data via Deadlock API, preprocessing and engineering features, and training predictive models to forecast winners.

--- image with accuracies ---

## Installation

### Prerequisites

* Python 3.10 or newer

### Windows

Open Windows PowerShell and copy-paste the following:

```bash
git clone https://github.com/Lev1231254/MatchPredictorDeadlock
cd MatchPredictorDeadlock
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook jupyter_notebooks/test_models.ipynb
```

### Linux

Open a terminal and copy-paste the following:

```bash
git clone https://github.com/Lev1231254/MatchPredictorDeadlock
cd MatchPredictorDeadlock
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook jupyter_notebooks/test_models.ipynb
```

After that, a notebook containing tests of different models should open.

--- screenshot of the notebook ---

## Details

### Technologies used
- Problem exploring: Jupyter Notebook
- Data & Pipeline: SQL, Python, pandas
- Modelling: scikit-learn, Gradient Boosting Classifier
- Visualization: seaborn

### Data Fetching

I fetched data from the Deadlock API data dumps:

https://deadlock-api.com/data-dumps

There, you can find a large dataset containing match data that looks like this:

--- data image ---

### Data Preprocessing

1. Initially, data from the Deadlock API is structured **per player**. This means that instead of one row per match, there is one row for each player who participated in the match.

   Each match is divided into 12 rows, so I merge these 12 rows into a single match record:

   --- preprocessed matches dataframe ---

2. I include the following features:

   * heroes
   * net worth of each hero since the previous timestamp
   * which team killed the Mid Boss since the previous timestamp

3. Since the state of a match changes over time, it is better to train a separate model for each minute of the game.

   To differentiate between game states, we use the `time_stamp_s` column. It records the state of the game at different timestamps.

   --- image explaining the `time_stamp_s` column and its relationship to net worth and Mid Boss kills ---

### Training Models

Simple models such as Logistic Regression are not well suited for this task because they cannot capture the complex interactions between heroes.
Instead, I use a **Gradient Boosting Classifier**.

I tuned the hyperparameters using a random search algorithm.
Average training time: XX minutes.

--- tuned vs. untuned (replace with full graph) ---

<img width="585" height="454" alt="image" src="https://github.com/user-attachments/assets/ab91dbb7-c788-4c60-98bc-6853369a569f" />

## Navigation

`jupyter_notebooks/` — notebooks used for dataset exploration and experimentation

`data/` — preprocessed data (empty in the GitHub repository to avoid storing large files)

`models_raw/` — untuned Gradient Boosting Classifier models

`models_tuned/` — tuned Gradient Boosting Classifier models

`pipeline/` — data fetching, preprocessing, and utility functions

`scripts/` — scripts for fetching data, saving datasets, training models, and saving trained models

