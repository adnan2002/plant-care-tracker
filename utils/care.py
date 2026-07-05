
import pandas as pd

from datetime import date as today_date, timedelta, datetime

from dateutil.relativedelta import relativedelta

from utils.load_plants import care_log_df, load_plants, save_care_log, load_due_log, save_due_log

due_log_df = load_due_log()

CARE_ACTIVITIES = {
    "watering": ("watering_frequency_days", "days"),
    "fertilizing": ("fertilizing_weeks", "weeks"),
    "repotting": ("repotting_months", "months"),
    "pruning": ("pruning_weeks", "weeks"),
}


def normalize_activity(activity):
    return str(activity).strip().lower()


def get_activity_schedule(plant, activity):
    activity = normalize_activity(activity)
    if activity not in CARE_ACTIVITIES:
        raise ValueError(f"Unknown care activity: {activity}")

    frequency_column, unit = CARE_ACTIVITIES[activity]
    return int(plant[frequency_column]), unit



def add_interval(date_str, value, unit):
    date = datetime.strptime(date_str, "%Y-%m-%d").date()

    if unit == "days":
        result = date + timedelta(days=value)
    elif unit == "weeks":
        result = date + timedelta(weeks=value)
    elif unit == "months":
        result = date + relativedelta(months=value)
    else:
        raise ValueError(f"Unsupported unit: {unit}")

    return result.strftime("%Y-%m-%d")


def add_due_log(due_log_df, plant_id, activity, value, unit, date_acquired=None):
    activity = normalize_activity(activity)
    if date_acquired is not None:
        base_date = date_acquired
    else:
        existing = due_log_df[
            (due_log_df["plant_id"] == plant_id)
            & (due_log_df["activity"] == activity)
        ]
        if existing.empty:
            raise ValueError(
                f"No date_acquired given and no existing due_log row for "
                f"plant_id={plant_id}, activity={activity}."
            )
        base_date = existing["due_date"].max()

    next_due_id = 1 if due_log_df.empty else int(due_log_df["due_id"].max()) + 1
    new_due_date = add_interval(base_date, value, unit)

    new_row = pd.DataFrame([{
        "due_id": next_due_id,
        "plant_id": plant_id,
        "due_date": new_due_date,
        "activity": activity,
    }])

    return pd.concat([due_log_df, new_row], ignore_index=True)



def update_due_log(due_log_df, plant_id, activity, value, unit, completed_date):
    activity = normalize_activity(activity)
    mask = (due_log_df["plant_id"] == plant_id) & (due_log_df["activity"] == activity)
    if not mask.any():
        raise ValueError(f"No due_log row to update for plant_id={plant_id}, activity={activity}")

    due_log_df.loc[mask, "due_date"] = add_interval(completed_date, value, unit)
    return due_log_df


def ensure_due_log_rows(due_log_df, plants_df):
    due_log_df = due_log_df.copy()
    due_log_df["plant_id"] = pd.to_numeric(due_log_df["plant_id"], errors="coerce")
    due_log_df["due_id"] = pd.to_numeric(due_log_df["due_id"], errors="coerce")
    due_log_df["activity"] = due_log_df["activity"].apply(normalize_activity)
    due_log_df = due_log_df.sort_values("due_id").drop_duplicates(
        subset=["plant_id", "activity"],
        keep="last",
    )

    for _, plant in plants_df.iterrows():
        plant_id = int(plant["plant_id"])
        for activity in CARE_ACTIVITIES:
            exists = (
                (due_log_df["plant_id"] == plant_id)
                & (due_log_df["activity"] == activity)
            ).any()
            if exists:
                continue

            value, unit = get_activity_schedule(plant, activity)
            due_log_df = add_due_log(
                due_log_df,
                plant_id=plant_id,
                activity=activity,
                value=value,
                unit=unit,
                date_acquired=plant["date_acquired"],
            )

    return due_log_df


def get_due_care_sections():
    plants = load_plants()
    due_logs = ensure_due_log_rows(load_due_log(), plants)
    save_due_log(due_logs)

    due_logs = due_logs.copy()
    plants = plants.copy()
    due_logs["plant_id"] = pd.to_numeric(due_logs["plant_id"], errors="coerce")
    plants["plant_id"] = pd.to_numeric(plants["plant_id"], errors="coerce")

    due_care = due_logs.merge(
        plants[["plant_id", "name", "location"]],
        on="plant_id",
        how="left",
    )
    due_care["due_date"] = pd.to_datetime(due_care["due_date"], errors="coerce")
    due_care["activity"] = due_care["activity"].str.title()

    today = pd.Timestamp(today_date.today())
    display_columns = ["plant_id", "name", "location", "activity", "due_date"]
    due_care = due_care[display_columns].sort_values(["due_date", "name", "activity"])

    past_due = due_care[due_care["due_date"] < today].copy()
    due = due_care[due_care["due_date"] >= today].copy()

    for frame in (past_due, due):
        frame["due_date"] = frame["due_date"].dt.date

    return past_due, due

def record_care(name, activity, date):
    plants = load_plants()
    plant_matches = plants.loc[plants["name"] == name, ["plant_id"]]

    if plant_matches.empty:
        raise ValueError(f"Unknown plant: {name}")

    plant = plants.loc[plants["name"] == name].iloc[0]
    plant_id = int(plant["plant_id"])
    activity = normalize_activity(activity)
    value, unit = get_activity_schedule(plant, activity)
    care_date = pd.Timestamp(date).date().isoformat()

    updated_due_log = update_due_log(
        load_due_log(),
        plant_id=plant_id,
        activity=activity,
        value=value,
        unit=unit,
        completed_date=care_date,
    )

    log_ids = pd.to_numeric(care_log_df["log_id"], errors="coerce")
    next_log_id = 1 if log_ids.dropna().empty else int(log_ids.max()) + 1

    care_log_df.loc[len(care_log_df)] = {
        "log_id": next_log_id,
        "plant_id": plant_id,
        "activity": activity,
        "date": care_date,
    }

    save_care_log()
    save_due_log(updated_due_log)
    return next_log_id
