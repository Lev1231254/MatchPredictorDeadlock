import tools

def fetch_heroes_data():
    heroes = tools.get_heroes_dataframe()
def fetch_match_data(time_stamp_s : int):

    features = '''match_id, match_outcome, winning_team, hero_id, team, 
            match_mode, average_badge_team0, "stats.time_stamp_s", "stats.net_worth", 
            "mid_boss.destroyed_time_s", "mid_boss.team_claimed"'''

    dataset = tools.get_match_dataframe(features, 1000)
    heroes = tools.get_heroes_dataframe()
