from pathlib import Path
import pandas as pd
from joblib import load


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


def test_model_accuracy(data_test_filename : str, model_filename : str):

    data_path = Path("../data") / data_test_filename
    model_path = Path("../models_raw") / model_filename

    dataset_test = pd.read_csv(data_path)
    model = load(model_path)
    
    data_test = dataset_test.drop(columns=["winning_team", "match_id"])
    target_test = dataset_test["winning_team"]


    predictions = model.predict(data_test)
    accuracy = (predictions==target_test).mean()

    return accuracy
