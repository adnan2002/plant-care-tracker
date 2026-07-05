import pandas as pd

from utils.care import add_due_log, get_seasonally_adjusted_schedule
from utils.storage import plants_df, save_plants, load_due_log, save_due_log

due_log_df = load_due_log()


def get_plant(plant_id):
    return plants_df.loc[plants_df["plant_id"] == plant_id].iloc[0]


def get_all_plants():
    return plants_df.copy()


def search_plant(query):
    return plants_df[
        plants_df['name'].str.contains(query, case=False, na=False) |
        plants_df['location'].str.contains(query, case=False, na=False)
    ]


def get_all_plant_names():
    return plants_df["name"].dropna().unique().tolist()


def get_plant_by_name(name):
    return plants_df.loc[plants_df["name"] == name].iloc[0]


def add_plant(
    name,
    location,
    date_acquired,
    watering_frequency_days,
    fertilizing_weeks,
    repotting_months,
    plant_type,
    pruning_weeks,
    sunlight_needs,
    photo_path="",
    plant_id=None,
):


    global due_log_df

    next_id = plant_id if plant_id is not None else (1 if plants_df.empty else int(plants_df["plant_id"].max()) + 1)

    plants_df.loc[len(plants_df)] = {
        "plant_id": next_id,
        "name": name,
        "location": location,
        "date_acquired": date_acquired,
        "watering_frequency_days": watering_frequency_days,
        "sunlight_needs": sunlight_needs,
        "photo_path": photo_path,
        "fertilizing_weeks": fertilizing_weeks,
        "repotting_months": repotting_months,
        "pruning_weeks": pruning_weeks,
        "plant_type": plant_type
    }

    save_plants()

    activities = [
        ("watering",    watering_frequency_days, "days"),
        ("fertilizing", fertilizing_weeks,        "weeks"),
        ("repotting",   repotting_months,         "months"),
        ("pruning",     pruning_weeks,             "weeks"),
    ]

    for activity, value, unit in activities:
        adjusted_value, adjusted_unit = get_seasonally_adjusted_schedule(
            plants_df.loc[plants_df["plant_id"] == next_id].iloc[0],
            activity,
            date_acquired,
        )
        due_log_df = add_due_log(
            due_log_df,
            plant_id=next_id,
            activity=activity,
            value=adjusted_value,
            unit=adjusted_unit,
            date_acquired=date_acquired,
        )

    save_due_log(due_log_df)
