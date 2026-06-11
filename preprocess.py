import tools
import pandas as pd
import numpy as np

def data_feature_preprocess(dataset : pd.DataFrame, heroes : pd.DataFrame, time_s : int) -> pd.DataFrame:
    hero_ids = heroes["id"].to_numpy()
    n_features = len(heroes) + 3
    
    curr_match_id = "0"
    row = [0 for i in range(n_features)]
    new_data_np = np.array([row])
           
    for i in range(len(dataset)):
        # normal params
        match_id = dataset.at[i, "match_id"]
        winning_team = dataset.at[i, "winning_team"]
        hero_id = dataset.at[i, "hero_id"]
        team = dataset.at[i, "team"]
        
        # params with time stamps
        # net worth
        stats_time_stamp_s = np.array(dataset.at[i, "stats.time_stamp_s"])
        stats_time_stamp_last_id = tools.find_biggest_lesser_num(stats_time_stamp_s, time_s)
        if stats_time_stamp_last_id == None: print("NO TIME STAMPS AT TIME: " + str(time_s) + "s")
            
        stats_net_worth = dataset.at[i, "stats.net_worth"]
        net_worth = stats_net_worth[stats_time_stamp_last_id]

        # mid boss
        mid_boss_destroyed_time_s = dataset.at[i, "mid_boss.destroyed_time_s"]
        mid_boss_last_id = tools.find_biggest_lesser_num(mid_boss_destroyed_time_s, time_s)
        
        if mid_boss_last_id == None: 
            mid_boss_team_claimed = 0
        else: 
            mid_boss_team_claimed = (dataset.at[i, "mid_boss.team_claimed"][mid_boss_last_id] == "Team0") * 2 - 1

        # each new match add new row
        if curr_match_id != match_id:
            new_data_np = np.append(new_data_np, [row], axis=0)
                
            row = [0 for i in range(n_features)]
            curr_match_id = match_id
            row[0] = curr_match_id
            row[1] = winning_team
            row[2] = mid_boss_team_claimed
            
        hero_row_id = (hero_ids == hero_id).nonzero()[0][0] + 3

        # change heroes net worth
        if team == "Team0":
            row[hero_row_id] = int(net_worth)
            
        else:
            row[hero_row_id] = -1 * int(net_worth)
        
    new_data_np = np.append(new_data_np, [row], axis=0)
    new_data_np = np.delete(new_data_np, [0,1], axis=0)

    columns = np.append(["match_id", "winning_team", "mid_boss.team_claimed"], hero_ids)

    new_data = pd.DataFrame(new_data_np, columns=columns)
    return new_data