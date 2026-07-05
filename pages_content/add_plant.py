import streamlit as st
from pathlib import Path

from utils.add_plant import add_plant
from utils.load_plants import plants_df


st.title("Add Plant")

with st.form("add_plant_form"):
    name = st.text_input("Name")
    plant_type = st.text_input("Plant Type")
    location = st.text_input("Location")
    date_acquired = st.date_input("Date acquired")
    watering_frequency_days = st.number_input("Watering frequency (days)", min_value=1, value=7, step=1)
    fertilizing_weeks = st.number_input("Fertlizing frequency (weeks)", min_value=1, step=1)
    repotting_months = st.number_input("Repotting frequency (months)", min_value=1, step=1)
    pruning_weeks = st.number_input("Prunning frequency (weeks)", min_value=1, step=1)
    sunlight_needs = st.selectbox("Sunlight needs", ["Low", "Medium", "High"])
    uploaded_photo = st.file_uploader("Photo", type=["png", "jpg", "jpeg", "webp"])

    submitted = st.form_submit_button("Add plant")

if submitted:
    name = name.strip()
    location = location.strip()

    if not name or not location or uploaded_photo is None:
        st.error("Please fill in all fields and upload a photo.")
        st.stop()

    next_id = 1 if plants_df.empty else int(plants_df["plant_id"].max()) + 1
    photo_path = ""
    upload_dir = Path(f"data/uploads/plants/{next_id:04d}")
    variants_dir = upload_dir / "progress"
    variants_dir.mkdir(parents=True, exist_ok=True)
    photo_file = upload_dir / "cover.jpg"
    photo_file.write_bytes(uploaded_photo.getvalue())
    photo_path = str(photo_file)

    add_plant(
        name=name,
        location=location,
        date_acquired=date_acquired.isoformat(),
        watering_frequency_days=int(watering_frequency_days),
        sunlight_needs=sunlight_needs,
        photo_path=photo_path,
        plant_type=plant_type,
        plant_id=next_id,
        fertilizing_weeks=fertilizing_weeks,
        pruning_weeks=pruning_weeks,
        repotting_months=repotting_months
    )
    st.success(f"Added {name}")
