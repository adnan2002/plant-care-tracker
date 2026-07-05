import streamlit as st

from utils.plants import get_all_plants

st.title("All Plants")



st.dataframe(get_all_plants())
