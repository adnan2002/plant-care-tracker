
import pandas as pd

from utils.storage import load_growth, save_growth


growth_df = load_growth()


# measurement_id,plant_id,date,height_cm,width_cm,leaf_count,notes


def record_growth_measurement(plant_id, date, height_cm, width_cm, leaf_count, notes=""):
    
    next_id = 1 if growth_df.empty else int(growth_df["measurement_id"].max()) + 1

    growth_df.loc[len(growth_df)] = {
        "measurement_id": next_id,
        "plant_id": plant_id,
        "date": date,
        "height_cm": height_cm,
        "width_cm": width_cm,
        "leaf_count": leaf_count,
        "notes": notes
    }

    save_growth(growth_df)



    
def get_growth_history(plant_id):
    history = load_growth()
    if history.empty:
        return history

    history = history[history["plant_id"] == plant_id].copy()
    if not history.empty:
        history["date"] = pd.to_datetime(history["date"])
        history = history.sort_values("date")
    return history


def get_growth_summary(plant_id):
    history = get_growth_history(plant_id)
    if history.empty:
        return {
            "measurements": 0,
            "latest_height_cm": None,
            "latest_width_cm": None,
        }

    latest = history.iloc[-1]
    return {
        "measurements": len(history),
        "latest_height_cm": latest["height_cm"],
        "latest_width_cm": latest["width_cm"],
    }
