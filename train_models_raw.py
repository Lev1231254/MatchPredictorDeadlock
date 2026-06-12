import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier
from joblib import dump


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

    dataset_files = [f.name for f in Path("data/").glob("matches*train.csv")]
    
    for dataset_file in dataset_files:
        time_stamp = dataset_file[7:-9] # filename : matches*train.csv

        dataset = pd.read_csv("data/" + dataset_file)
        data = dataset.drop(columns=["winning_team", "match_id"])
        target = dataset["winning_team"]

        model = classifier.fit(data, target)
        dump(model, "models_raw/GBC" + str(time_stamp) + ".joblib")

    print("Models are trained and saved.")

else:
    print("Process terminated")