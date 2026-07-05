import streamlit as st

from utils.growth import record_growth_measurement
from utils.get_plant import get_all_plant_names, get_plant_by_name


st.title("Growth Tracker")

names = get_all_plant_names()

if not names:
    st.info("Add a plant for tracking growth.")
    st.stop()

with st.form("add_growth"):
    name = st.selectbox("Plant", names)
    date = st.date_input("Date")
    height_cm = st.number_input("Height (cm)", min_value=0, step=1)
    width_cm = st.number_input("Width (cm)", min_value=0, step=1)
    leaf_count = st.number_input("Leaf Count", min_value=0, step=1)
    notes = st.text_input("Notes")

    submitted = st.form_submit_button("Add growth")

if submitted:
    plant_id = get_plant_by_name(name)["plant_id"]
    record_growth_measurement(
        plant_id,
        date=date,
        height_cm=height_cm,
        width_cm=width_cm,
        leaf_count=leaf_count,
        notes=notes,
    )
    st.success(f"Added growth for {name}")
