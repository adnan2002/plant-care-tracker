from datetime import date as date_type
from math import ceil


def get_season(value):
    if isinstance(value, str):
        value = date_type.fromisoformat(value)

    month = value.month
    if month in (12, 1, 2):
        return "winter"
    if month in (3, 4, 5):
        return "spring"
    if month in (6, 7, 8):
        return "summer"
    return "autumn"


def adjust_frequency_for_season(activity, base_value, unit, plant_type, season):
    activity = str(activity).strip().lower()
    plant_type = str(plant_type or "").strip().lower()
    season = str(season).strip().lower()

    multiplier = 1.0

    if activity == "watering":
        if season == "winter":
            if plant_type in {"cactus", "succulent"}:
                multiplier = 1.5
            else:
                multiplier = 1.2
        elif season == "summer" and plant_type in {"fern", "tropical"}:
            multiplier = 0.9

    if activity == "fertilizing":
        if season == "winter":
            multiplier = 2.0
        elif season in {"spring", "summer"} and plant_type in {"flowering", "tropical", "herb"}:
            multiplier = 0.75

    adjusted = max(1, ceil(float(base_value) * multiplier))
    return adjusted


def get_seasonal_care_reminders(plant_type, season):
    plant_type = str(plant_type or "").strip().lower()
    season = str(season).strip().lower()

    reminders = []

    if season == "winter":
        reminders.append("Reduce fertilizing and watch for slower growth.")
        if plant_type in {"cactus", "succulent"}:
            reminders.append("Let the soil dry fully between waterings.")
        if plant_type in {"tropical", "fern"}:
            reminders.append("Increase humidity with a tray or humidifier.")
    elif season == "spring":
        reminders.append("Resume active feeding as growth picks up.")
        if plant_type in {"flowering", "herb"}:
            reminders.append("Support new blooms or foliage with steady light and water.")
    elif season == "summer":
        reminders.append("Check moisture more often during hot spells.")
        if plant_type in {"tropical", "fern"}:
            reminders.append("Watch for heat stress and keep humidity stable.")
    else:
        reminders.append("Prepare for slower growth and reduce feeding gradually.")

    if not reminders:
        reminders.append("Follow the normal care routine for this plant.")

    return reminders