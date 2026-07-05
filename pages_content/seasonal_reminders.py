from datetime import date as today_date

import pandas as pd
import streamlit as st

from utils.care import CARE_ACTIVITIES, get_activity_schedule
from utils.plants import get_all_plants, get_plant_by_name, get_all_plant_names
from utils.seasons import adjust_frequency_for_season, get_season, get_seasonal_care_reminders


st.title("Seasonal Reminders")

plants = get_all_plants().copy()
if plants.empty:
    st.info("Add a plant first.")
    st.stop()

view_mode = st.radio("View reminders for", ["One plant", "All plants"], horizontal=True)
current_date = today_date.today()
current_season = get_season(current_date)


def render_plant(plant):
    plant_name = plant["name"]
    plant_type = plant.get("plant_type", "")

    st.subheader(plant_name)
    st.caption(f"Plant type: {plant_type or 'Unknown'} | Season: {current_season.title()}")

    rows = []
    for activity in CARE_ACTIVITIES:
        base_value, unit = get_activity_schedule(plant, activity)
        adjusted_value = adjust_frequency_for_season(activity, base_value, unit, plant_type, current_season)
        rows.append({
            "Activity": activity.title(),
            "Base interval": f"{base_value} {unit}",
            "Seasonal interval": f"{adjusted_value} {unit}",
        })

    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True)

    st.markdown("**Seasonal reminders**")
    for reminder in get_seasonal_care_reminders(plant_type, current_season):
        st.write(f"- {reminder}")


if view_mode == "One plant":
    names = get_all_plant_names()
    selected_name = st.selectbox("Plant", names)
    render_plant(get_plant_by_name(selected_name))
else:
    for _, plant in plants.iterrows():
        with st.expander(str(plant["name"]), expanded=False):
            render_plant(plant)
