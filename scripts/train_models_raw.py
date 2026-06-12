from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump
import pipeline.tools as tools

columns_preprocessor = make_column_transformer(
        (OneHotEncoder(handle_unknown="ignore"), ["mid_boss.team_claimed"]),
        remainder="passthrough"
    )

classifier = make_pipeline(
        columns_preprocessor,
        GradientBoostingClassifier()
    )


safety_check = input("Do you want to retrain models? (Y/n)\n")

if safety_check == "Y":
    print("Training models...")

    dataset_files = ["data/" + f.name for f in Path("data/").glob("matches*train.csv")]
    
    for dataset_file in dataset_files:
        time_stamp = tools.extract_match_timestamp(dataset_file)

        dataset = pd.read_csv(dataset_file)

        data = dataset.drop(columns=["winning_team", "match_id"])
        target = dataset["winning_team"]

        model = classifier.fit(data, target)
        dump(model, "models_raw/GBC" + str(time_stamp) + ".joblib")

    print("Models are trained and saved.")

else:
    print("Process terminated")