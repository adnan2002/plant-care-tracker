import pandas as pd
import streamlit as st

from utils.plants import get_all_plant_names, get_all_plants, get_plant_by_name
from utils.storage import load_growth


st.title("Growth Chart")

names = get_all_plant_names()

if not names:
    st.info("Add a plant for tracking growth.")
    st.stop()

growth_df = load_growth()

if growth_df.empty:
    st.info("No growth measurements recorded yet.")
    st.stop()

selected_plants = st.multiselect(
    "Choose plant(s) to compare",
    options=names,
    default=names[:1],
)

if not selected_plants:
    st.info("Select at least one plant to view its growth history.")
    st.stop()

plant_lookup = get_all_plants()[["plant_id", "name"]].dropna()
id_to_name = dict(zip(plant_lookup["plant_id"], plant_lookup["name"]))
selected_ids = [get_plant_by_name(plant_name)["plant_id"] for plant_name in selected_plants]

chart_df = growth_df[growth_df["plant_id"].isin(selected_ids)].copy()

if chart_df.empty:
    st.info("No growth measurements found for the selected plant(s).")
    st.stop()

chart_df["date"] = pd.to_datetime(chart_df["date"])
chart_df["plant_name"] = chart_df["plant_id"].map(id_to_name)

height_chart = chart_df.pivot_table(index="date", columns="plant_name", values="height_cm", aggfunc="last").sort_index()

width_chart = chart_df.pivot_table(index="date", columns="plant_name", values="width_cm", aggfunc="last").sort_index()

st.caption("Each line represents a selected plant.")

st.markdown("**Height (cm)**")

st.line_chart(height_chart)

st.markdown("**Width (cm)**")

st.line_chart(width_chart)
