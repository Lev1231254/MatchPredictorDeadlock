import pandas as pd
import fetch_data

fetch_data.get_heroes_dataframe().to_csv("data\heroes.csv")

