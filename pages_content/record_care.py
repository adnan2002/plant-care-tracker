from datetime import date as today_date

import streamlit as st

from utils.plants import get_all_plant_names
from utils.care import record_care

st.title("Record Care")
st.caption("Recording care recalculates that activity's next due date from the date entered.")


names = get_all_plant_names()

if not names:
    st.info("Add a plant before recording care.")
    st.stop()

with st.form("record_care_form"):
    name = st.selectbox("Plant", names)
    activity = st.selectbox("Activity", ["Watering", "Fertilizing", "Repotting", "Pruning"])
    date = st.date_input("Date", max_value=today_date.today())
    submitted = st.form_submit_button("Record care")

if submitted:
    try:
        record_care(name=name, activity=activity, date=date)
        st.success(f"Recorded {activity.lower()} for {name} on {date.isoformat()}")
    except ValueError as error:
        st.error(str(error))
