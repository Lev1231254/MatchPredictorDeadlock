import pandas as pd
import pipeline.fetch_data as fetch_data
import pipeline.preprocess as preprocess

# save heroes table
heroes = fetch_data.get_heroes_dataframe()
heroes.to_csv("data/heroes.csv")


# save preprocessed matches
LIMIT = 1000

features = '''match_id, match_outcome, winning_team, hero_id, team, 
        match_mode, average_badge_team0, "stats.time_stamp_s", "stats.net_worth", 
        "mid_boss.destroyed_time_s", "mid_boss.team_claimed"'''
time_stamps = [500, 1000, 1500]

for time_stamp in time_stamps:
    data = fetch_data.get_match_dataframe(features, LIMIT)
    data_preprocessed = preprocess.data_feature_preprocess(data, heroes, time_stamp)
    data_preprocessed.to_csv("data/matches" + str(time_stamp) + ".csv", index=False)