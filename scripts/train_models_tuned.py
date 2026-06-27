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
from scipy.stats import loguniform, randint
from sklearn.model_selection import RandomizedSearchCV
import time

columns_preprocessor = make_column_transformer(
        (OneHotEncoder(handle_unknown="ignore"), ["mid_boss.team_claimed"]),
        remainder="passthrough"
    )

classifier = make_pipeline(
        columns_preprocessor,
        GradientBoostingClassifier()
    )


param_distributions = {
    "gradientboostingclassifier__learning_rate" : loguniform(1e-2, 1),
    "gradientboostingclassifier__n_estimators" : randint(64, 512),
    "gradientboostingclassifier__min_samples_leaf" : randint(1, 256),
    "gradientboostingclassifier__min_samples_split" : randint(2, 12)
}

NUM_ITERATIONS = 200
NUM_FOLDS = 5

safety_check = input("\nTraining tuned models takes a lot of time. Do you want to retrain tuned models? (Y/n)\n")

if safety_check == "Y":
    print("Training models...")

    loaded_time_stamps = [1000, 1020]
    dataset_files = ["data/" + f.name for f in Path("data/").glob("matches*train.csv")]
    
    for dataset_file in dataset_files:

        # load dataset
        time_stamp = tools.extract_match_timestamp(dataset_file)
        if (time_stamp in loaded_time_stamps):
            continue
        

        dataset = pd.read_csv(dataset_file)

        data = dataset.drop(columns=["winning_team", "start_time"])
        target = dataset["winning_team"]

        # train model
        start = time.time()

        print(str(time_stamp) + " seconds: ", end="")
        model_random_search = RandomizedSearchCV(
            classifier,
            param_distributions=param_distributions,
            n_iter=NUM_ITERATIONS,
            cv=NUM_FOLDS,
            verbose=1
        )
        model_random_search.fit(data, target)

        end = time.time()
        print("elapsed time minutes " + str((end - start)//60))

        # save results and model
        cv_results = tools.get_random_search_results(model_random_search, param_distributions)
        cv_res_file = "models_tuned/cv_res" + str(time_stamp) + ".csv"
        cv_results.to_csv(cv_res_file, index=False)

        model_file = "models_tuned/GBC" + str(time_stamp) + ".joblib"
        dump(model_random_search, model_file)

    print("Models are trained and saved.\n")

else:
    print("Process terminated")