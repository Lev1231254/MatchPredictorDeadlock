import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingClassifier

# don't retrain models, if you don't know what you are doing

safety_check = input("Retraining new models will take some time. Do you want to do it? (Y/n)\n")

if safety_check == "Y":

    dataset_files = time_stamps = [f.name for f in Path("data/").glob("matches*.csv")]
    
    for dataset_file in dataset_files:
        dataset = pd.read_csv(dataset_file)
        data_train, data_test, target_train, target_test = train_test_split(dataset, test_size=0.2)
        

else:
    print("Process terminated")