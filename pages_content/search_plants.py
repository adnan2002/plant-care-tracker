import streamlit as st

from utils.plants import search_plant

st.title("Search Plants")


with st.form("search_plants_form"):
    query = st.text_input("Search").strip()
    submitted = st.form_submit_button("Search")

if submitted:
    st.dataframe(search_plant(query))
