import sys
from pathlib import Path

project_root = Path().resolve().parent

sys.path.append(str(project_root))

from pathlib import Path
import pandas as pd
from joblib import load, dump
from sklearn.model_selection import RandomizedSearchCV, cross_validate


def find_biggest_lesser_num(arr, num):
    # arr is sorted
    if len(arr) == 0: return None
    if min(arr) > num: return None
        
    for i in range(1, len(arr)):
        if arr[i] > num:
            return i - 1
            
    return len(arr) - 1


def find_all_time_stamps():
    time_stamps = [int(f.name[7:-4]) for f in Path("data/").glob("matches*.csv")]
    time_stamps.sort()
    return time_stamps


def test_model_accuracy(data_test_filename : str, model_filename : str, model_type):

    data_path = Path("../data") / data_test_filename
    model_path = Path("../models_" + model_type) / model_filename

    dataset_test = pd.read_csv(data_path)
    model = load(model_path)

    data_test = dataset_test.drop(columns=["winning_team", "start_time"])
    target_test = dataset_test["winning_team"]


    predictions = model.predict(data_test)
    accuracy = (predictions==target_test).mean()

    return accuracy


def extract_match_timestamp(filename : str) -> str:
    # matchesXX.csv -> XX
    if "test" in filename:
        return int(filename.split("matches")[1].split("test.csv")[0])
    elif "train" in filename:
        return int(filename.split("matches")[1].split("train.csv")[0])
    return None

def extract_model_timestamp(filename : str) -> str:
    # matchesXX.csv -> XX
    return int(filename.split("GBC")[1].split(".joblib")[0])


def get_sorted_files(model : str, model_type : str):
    data_test_files = sorted(
        [f.name for f in Path("../data/").glob("matches*test.csv")],
        key = lambda f : extract_match_timestamp(f)
    )
    model_files = sorted(
        [f.name for f in Path("../models_" + model_type + "/").glob(model + "*.joblib")],
        key = lambda f : extract_model_timestamp(f)
    )
    return data_test_files, model_files


def get_sorted_accuracies(model : str, model_type : str):
    accuracies = []

    data_test_filenames, model_filenames = get_sorted_files(model, model_type)
    time_stamps = [extract_match_timestamp(f) for f in data_test_filenames]

    pairs = list(zip(data_test_filenames, model_filenames))

    for data_test_filename, model_filename in pairs:

        accuracy = test_model_accuracy(data_test_filename, model_filename, model_type)
        accuracies.append(accuracy) 

    return pd.DataFrame({"Accuracy" : accuracies, "Time stamps in seconds" : time_stamps})



def change_param_names(param_name):
        if "__" in param_name:
            return param_name.rsplit("__")[1]
        return param_name


def get_random_search_results(random_search : RandomizedSearchCV, param_distributions):
    cv_results = pd.DataFrame(random_search.cv_results_).sort_values("mean_test_score", ascending=False)

    columns = [f"param_{param}" for param in param_distributions.keys()]
    columns += ["mean_test_score", "std_test_score", "rank_test_score"]

    cv_results = cv_results[columns]

    cv_results = cv_results.rename(change_param_names, axis=1)
    return cv_results


def df_seconds_to_minutes(df : pd.DataFrame):
    df["Time stamps in seconds"] = (df["Time stamps in seconds"].astype(int) // 60).astype(str)
    return df.rename(columns={"Time stamps in seconds" : "Time stamps in minutes"})


def remove_multiple_elements(target_arr, elements_to_delete):
    for element in elements_to_delete:
        target_arr.remove(element)
    return target_arr
