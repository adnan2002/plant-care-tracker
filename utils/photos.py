import os

import pandas as pd

from utils.storage import load_photos, save_photos


photos_df = load_photos()


def add_progress_photo(plant_id, date, file_path, caption):
    global photos_df

    next_id = 1 if photos_df.empty else int(photos_df["photo_id"].max()) + 1

    photos_df.loc[len(photos_df)] = {
        "photo_id": next_id,
        "plant_id": plant_id,
        "date": pd.to_datetime(date).date().isoformat(),
        "file_path": str(file_path),
        "caption": caption or "",
    }

    save_photos(photos_df)


def get_progress_photos(plant_id):
    history = load_photos()
    if history.empty:
        return history

    history = history[history["plant_id"] == plant_id].copy()
    if not history.empty:
        history["date"] = pd.to_datetime(history["date"], errors="coerce")
        history = history.sort_values(["date", "photo_id"], ascending=[False, False])
    return history


def store_uploaded_progress_photo(plant_id, uploaded_file):
    progress_dir = f"data/uploads/plants/{plant_id:04d}/progress"
    os.makedirs(progress_dir, exist_ok=True)

    _, ext = os.path.splitext(uploaded_file.name)
    suffix = ext or ".jpg"
    next_number = len(os.listdir(progress_dir)) + 1
    destination = os.path.join(progress_dir, f"progress_{next_number:04d}{suffix}")
    with open(destination, "wb") as handle:
        handle.write(uploaded_file.getvalue())
    return str(destination)
