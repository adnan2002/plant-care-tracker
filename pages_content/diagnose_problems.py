import streamlit as st

from utils.diagnosis import diagnose_plant
from utils.get_plant import get_all_plants, get_plant_by_name


st.title("Diagnose Problems")

plants = get_all_plants().copy()
if plants.empty:
    st.info("Add a plant first.")
    st.stop()

common_symptoms = [
    "yellow leaves",
    "brown tips",
    "wilting",
    "spots",
    "pests",
    "leggy growth",
    "root rot smell",
    "dry soil",
    "shriveled pads",
    "mushy stem",
    "dropping leaves",
    "no blooms",
]

mode = st.radio("Diagnose by", ["Plant", "Plant type"], horizontal=True)

if mode == "Plant":
    selected_name = st.selectbox("Plant", plants["name"].dropna().tolist())
    plant = get_plant_by_name(selected_name)
    selected_plant_type = plant.get("plant_type", "")
    st.caption(f"Plant type: {selected_plant_type or 'Unknown'}")
else:
    available_types = sorted({str(value).strip() for value in plants["plant_type"].dropna().tolist() if str(value).strip()})
    if not available_types:
        st.info("No plant types available yet.")
        st.stop()
    selected_plant_type = st.selectbox("Plant type", available_types)

selected_symptoms = st.multiselect("Symptoms", common_symptoms)

if st.button("Diagnose"):
    results = diagnose_plant(selected_symptoms, plant_type=selected_plant_type)

    if not results:
        st.info("No matches found in the current rule set.")
    else:
        st.subheader("Likely problems")
        for result in results:
            st.markdown(f"**{result['problem']}**")
            st.caption(f"Severity: {result['severity'].title()} | Matched: {', '.join(result['matched_symptoms'])}")
            st.write(result["recommendation"])
