import pandas as pd
import numpy as np
import pipeline.fetch_data as fetch_data
import pipeline.preprocess as preprocess


safety_check = input("Saving datasets will take some time. Do you want to do it? (Y/n)\n")
if safety_check == "Y":
        print("Saving datasets...")
        # save heroes table
        heroes = fetch_data.get_heroes_dataframe()
        heroes.to_csv("data/heroes.csv")


        # save preprocessed matches
        LIMIT = 10000

        features = '''match_id, match_outcome, winning_team, hero_id, team, 
                match_mode, average_badge_team0, "stats.time_stamp_s", "stats.net_worth", 
                "mid_boss.destroyed_time_s", "mid_boss.team_claimed"'''
        time_stamps = [500, 1000, 1500]

        for time_stamp in time_stamps:
                data = fetch_data.get_match_dataframe(features, LIMIT)
                data_preprocessed = preprocess.data_feature_preprocess(data, heroes, time_stamp)

                data_preproc_test = data_preprocessed.sample(frac=0.2)
                data_preproc_train = data_preprocessed.drop(data_preproc_test.index)
                data_preproc_test.to_csv("data/matches" + str(time_stamp) + "test.csv", index=False)
                data_preproc_train.to_csv("data/matches" + str(time_stamp) + "train.csv", index=False)

        print("Datasets are saved")
else:
    print("Process terminated")