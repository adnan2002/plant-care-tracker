from datetime import date as date_type
from math import ceil
from pathlib import Path
import pandas as pd

SEASONAL_RULES_CSV = Path("data/seasonal_rules.csv")


def normalize(value):
    if value is None:
        value = ""
    return str(value).strip().lower()


def clean_reminder(value):
    if value is None:
        value = ""
    return str(value).strip()


def load_rules():
    if not SEASONAL_RULES_CSV.exists():
        cols = ["rule_id", "plant_type", "season", "activity", "multiplier", "reminder"]
        return pd.DataFrame(columns=cols)

    df = pd.read_csv(SEASONAL_RULES_CSV)
    df = df.fillna("")

    # clean up the text columns so matching works properly later
    for col in ["plant_type", "season", "activity"]:
        if col in df.columns:
            df[col] = df[col].map(normalize)

    if "reminder" in df.columns:
        df["reminder"] = df["reminder"].map(clean_reminder)

    if "multiplier" in df.columns:
        df["multiplier"] = pd.to_numeric(df["multiplier"], errors="coerce")

    return df


SEASONAL_RULES = load_rules()


def season_matches(rules, season):
    season = normalize(season)
    return rules[rules["season"] == season]


def plant_type_matches(rules, plant_type):
    plant_type = normalize(plant_type)

    matching = rules[rules["plant_type"].isin([plant_type, "", "any"])]

    if plant_type != "":
        exact_rows = matching[matching["plant_type"] == plant_type]
        if len(exact_rows) > 0:
            generic_rows = matching[matching["plant_type"].isin(["", "any"])]
            return exact_rows, generic_rows

    empty_exact = pd.DataFrame(columns=rules.columns)
    generic_rows = matching[matching["plant_type"].isin(["", "any"])]
    return empty_exact, generic_rows


def activity_matches(rules, activity):
    activity = normalize(activity)
    if activity != "":
        return rules[rules["activity"].isin([activity, ""])]
    else:
        return rules[rules["activity"] == ""]


def get_season(value):
    if isinstance(value, str):
        value = date_type.fromisoformat(value)

    month = value.month

    if month == 12 or month == 1 or month == 2:
        return "winter"
    elif month in (3, 4, 5):
        return "spring"
    elif month in (6, 7, 8):
        return "summer"
    else:
        return "autumn"


def adjust_frequency_for_season(activity, base_value, plant_type, season):
    season_rules = season_matches(SEASONAL_RULES, season)
    rules = activity_matches(season_rules, activity)

    exact, generic = plant_type_matches(rules, plant_type)

    if not exact.empty:
        selected = exact
    else:
        selected = generic

    multiplier = 1.0
    if not selected.empty and "multiplier" in selected.columns:
        valid_multipliers = selected["multiplier"].dropna()
        if len(valid_multipliers) > 0:
            multiplier = float(valid_multipliers.iloc[0])

    adjusted = ceil(float(base_value) * multiplier)
    if adjusted < 1:
        adjusted = 1

    return adjusted


def get_seasonal_care_reminders(plant_type, season):
    season_rules = season_matches(SEASONAL_RULES, season)
    no_activity_rules = season_rules[season_rules["activity"] == ""]

    exact, generic = plant_type_matches(no_activity_rules, plant_type)
    selected = pd.concat([generic, exact], ignore_index=True)

    reminders = []
    if not selected.empty and "reminder" in selected.columns:
        for r in selected["reminder"].tolist():
            if r:
                reminders.append(r)
        reminders = list(dict.fromkeys(reminders))

    if len(reminders) > 0:
        return reminders

    fallback = {
        "winter": "Reduce fertilizing and watch for slower growth.",
        "spring": "Resume active feeding as growth picks up.",
        "summer": "Check moisture more often during hot spells.",
        "autumn": "Prepare for slower growth and reduce feeding gradually.",
    }

    return [fallback.get(normalize(season), "Follow the normal care routine for this plant.")]