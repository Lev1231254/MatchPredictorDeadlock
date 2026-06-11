import duckdb
import pandas as pd

def get_match_dataframe(features : str, limit : int):
    limit = str(limit)
    DUCKLAKE_URL = "ducklake:https://s3-cache.deadlock-api.com/db-snapshot/public/db_snapshot.ducklake"


    with duckdb.connect() as con:
        con.execute("""
            INSTALL ducklake; LOAD ducklake;
            INSTALL httpfs; LOAD httpfs;
            CREATE OR REPLACE SECRET deadlock_s3 (
                TYPE S3, KEY_ID '', SECRET '',
                ENDPOINT 's3-cache.deadlock-api.com', URL_STYLE 'path', USE_SSL true
            );
        """)
        con.execute(f"ATTACH '{DUCKLAKE_URL}' AS db (READ_ONLY)")
        con.execute("USE db.main")

        # Tables are now queryable directly:
        con.sql("SHOW TABLES").show()
        
        dataset = con.sql( 'SELECT ' + features + " FROM read_parquet(['s3://db-snapshot/public/match_player/match_player_84.parquet']) " +
                        'WHERE average_badge_team0 > 90 AND average_badge_team1 > 90 AND match_outcome = \'TeamWin\' '
                        'LIMIT ' + limit + ';').df()
        return dataset
        heroes = con.sql("SELECT * FROM heroes").df()
        heroes.index = heroes["id"]

    num_heroes = len(heroes)

def get_heroes_dataframe():
    DUCKLAKE_URL = "ducklake:https://s3-cache.deadlock-api.com/db-snapshot/public/db_snapshot.ducklake"


    with duckdb.connect() as con:
        con.execute("""
            INSTALL ducklake; LOAD ducklake;
            INSTALL httpfs; LOAD httpfs;
            CREATE OR REPLACE SECRET deadlock_s3 (
                TYPE S3, KEY_ID '', SECRET '',
                ENDPOINT 's3-cache.deadlock-api.com', URL_STYLE 'path', USE_SSL true
            );
        """)
        con.execute(f"ATTACH '{DUCKLAKE_URL}' AS db (READ_ONLY)")
        con.execute("USE db.main")

        heroes = con.sql("SELECT * FROM heroes").df()
        heroes.index = heroes["id"]
        return heroes
    

def find_biggest_lesser_num(arr, num):
    # arr is sorted
    if len(arr) == 0: return None
    if min(arr) > num: return None
        
    for i in range(1, len(arr)):
        if arr[i] > num:
            return i - 1
            
    return len(arr) - 1
