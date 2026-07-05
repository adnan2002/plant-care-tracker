import os

import streamlit as st

from utils.plants import get_all_plant_names, get_plant_by_name
from utils.photos import add_progress_photo, get_progress_photos, store_uploaded_progress_photo


st.title("Progress Photos")

names = get_all_plant_names()

if not names:
    st.info("Add a plant before uploading progress photos.")
    st.stop()


def show_cover_preview(plant_name):
    plant = get_plant_by_name(plant_name)
    cover_value = str(plant.get("photo_path", "")).strip()
    cover_path = cover_value if cover_value else ""

    if cover_path and os.path.exists(cover_path):
        st.caption("Base image")
        st.image(cover_path, width=300)
    else:
        st.caption("No base image found for this plant.")

with st.form("progress_photo_form"):
    name = st.selectbox("Plant", names)
    show_cover_preview(name)
    date = st.date_input("Date")
    caption = st.text_input("Caption")
    uploaded_photo = st.file_uploader("Upload photo", type=["png", "jpg", "jpeg", "webp"])
    existing_path = st.text_input("Or existing file path")

    submitted = st.form_submit_button("Save progress photo")

if submitted:
    plant_id = get_plant_by_name(name)["plant_id"]

    if uploaded_photo is not None:
        file_path = store_uploaded_progress_photo(plant_id, uploaded_photo)
    else:
        file_path = existing_path.strip()

    if not file_path:
        st.error("Upload a photo or enter an existing file path.")
        st.stop()

    if uploaded_photo is None and not os.path.exists(file_path):
        st.error("The provided file path does not exist.")
        st.stop()

    add_progress_photo(plant_id, date=date, file_path=file_path, caption=caption)
    st.success(f"Saved progress photo for {name}")

st.divider()
st.subheader("Previous progress photos")

selected_name = st.selectbox("View photos for", names, key="progress_photo_history")
show_cover_preview(selected_name)
selected_plant_id = get_plant_by_name(selected_name)["plant_id"]
history = get_progress_photos(selected_plant_id)

if history.empty:
    st.info("No progress photos for this plant yet.")
else:
    for _, row in history.iterrows():
        st.caption(f"{row['date'].date().isoformat()} - {row['caption'] or 'No caption'}")
        st.image(str(row["file_path"]), width=300)
