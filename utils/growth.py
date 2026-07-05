
import pandas as pd

from utils.load_plants import load_growth


growth_df = load_growth()





def record_growth_measurement(plant_id, date, height_cm, width_cm, leaf_count, notes):
    
    next_id = plant_id if plant_id is not None else (1 if plants_df.empty else int(plants_df["plant_id"].max()) + 1)

    
def get_growth_history(plant_id):
    return
def get_growth_summary(plant_id):
    return