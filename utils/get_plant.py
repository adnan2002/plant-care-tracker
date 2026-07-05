import pandas as pd

from utils.load_plants import plants_df


def get_plant(plant_id):
    return plants_df.loc[plants_df["plant_id"] == plant_id].iloc[0]


def get_all_plants():
    return plants_df

def search_plant(query):
    return plants_df[
        plants_df['name'].str.contains(query, case=False, na=False) |
        plants_df['location'].str.contains(query, case=False, na=False)
    ]

def get_all_plant_names():
    return plants_df["name"].dropna().unique().tolist()


