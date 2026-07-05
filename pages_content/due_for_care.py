import streamlit as st

from utils.care import get_due_care_sections


st.title("Due For Care")

past_due, due = get_due_care_sections()

st.subheader("Past Due")
if past_due.empty:
    st.info("No care activities are past due.")
else:
    st.dataframe(past_due[["name", "location", "activity", "due_date"]], hide_index=True, use_container_width=True)

st.subheader("Due")
if due.empty:
    st.info("No upcoming care activities found.")
else:
    st.dataframe(
        due[["name", "location", "activity", "due_date"]],
        hide_index=True,
        use_container_width=True,
    )
