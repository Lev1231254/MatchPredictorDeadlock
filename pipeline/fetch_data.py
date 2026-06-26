from pathlib import Path
import sys

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import duckdb


def get_match_dataframe(features : str, limit : int, time_start : str, time_end : str):
    
    DUCKLAKE_URL = "ducklake:https://s3-cache.deadlock-api.com/fast/db_snapshot.ducklake"

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
        # read_parquet(['s3://db-snapshot/public/match_player/match_player_88.parquet']
        dataset = con.sql(f"""
            SELECT {features}
            FROM read_parquet('data/*.parquet')
            WHERE
                match_outcome = 'TeamWin'
                AND average_badge_team0 >= 100
                AND average_badge_team1 >= 100
                AND start_time BETWEEN
                    TIMESTAMPTZ {time_start}
                    AND TIMESTAMPTZ {time_end}
            LIMIT {limit}
        """).df()
    

def get_heroes_dataframe():
    DUCKLAKE_URL = "ducklake:https://s3-cache.deadlock-api.com/fast/db_snapshot.ducklake"


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
    

def get_match_dataframe_from_file(features: str, limit: int, time_start: str, time_end: str):

    with duckdb.connect() as con:
        dataset = con.sql(f"""
            SELECT {features}
            FROM read_parquet('data_raw/*.parquet')
            WHERE
                match_outcome = 'TeamWin'
                AND average_badge_team0 >= 100
                AND average_badge_team1 >= 100
                AND start_time BETWEEN
                    TIMESTAMPTZ {time_start}
                    AND TIMESTAMPTZ {time_end}
            LIMIT {limit}
        """).df()
        

    return dataset