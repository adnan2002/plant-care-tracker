import streamlit as st

st.set_page_config(page_title="Plant Tracker", layout="wide")

add_plant_page = st.Page("pages_content/add_plant.py", title="Add Plant", default=True)
record_care_page = st.Page("pages_content/record_care.py", title="Record Care")
due_for_care_page = st.Page("pages_content/due_for_care.py", title="Due For Care")
search_plants_page = st.Page("pages_content/search_plants.py", title="Search Plants")
all_plants_page = st.Page("pages_content/all_plants.py", title="All Plants")
growth_page = st.Page("pages_content/growth_tracker.py", title="Growth Tracker")
growth_chart_page = st.Page("pages_content/growth_chart.py", title="Growth Chart")
progress_photos_page = st.Page("pages_content/progress_photos.py", title="Progress Photos")


pg = st.navigation(
    {
        "Plants": [add_plant_page, search_plants_page, all_plants_page],
        "Care": [record_care_page, due_for_care_page],
        "Growth": [growth_page, growth_chart_page, progress_photos_page]
    }
)

pg.run()
