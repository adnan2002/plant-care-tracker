import streamlit as st


st.title("Growth Tracker")

# Enter date, height, width, leaf count, and notes.

with st.form("add_growth"):
    date = st.date_input("Date")
    height_cm = st.number_input("Height (cm)", min_value=0, step=1)
    wdith_cm = st.number_input("Width (cm)", min_value=0, step=1)
    leaf_count = st.number_input("Leaf Count", min_value=0, step=1)
    notes = st.text_input("Notes", min_value=1, value=7, step=1)

    submitted = st.form_submit_button("Add growth")

if submitted:

    

