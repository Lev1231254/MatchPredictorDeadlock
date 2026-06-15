import duckdb


def get_match_dataframe(features : str, limit : int, time_start : str, time_end : str):
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
        # read_parquet(['s3://db-snapshot/public/match_player/match_player_88.parquet']
        dataset = con.sql( 'SELECT ' + features + " FROM match_player " +
                        '''
                        WHERE 
                            match_outcome = \'TeamWin\' 
                            AND start_time BETWEEN
                                TIMESTAMPTZ ''' + time_start + '''
                            AND TIMESTAMPTZ ''' + time_end
                         + 
                        ' LIMIT ' + str(limit) + ';').df()
        return dataset
    

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