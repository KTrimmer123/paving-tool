
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel data
df = pd.read_excel("Paving Tool.xlsx", sheet_name="Sheet1", header=None)

# --- Extract System A/B table (rows 3–8, columns A–E) ---
data_ab = df.iloc[3:9, 0:5].copy()
data_ab.columns = ['Loading Category', 'Block/Laying Course (mm)', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)', 'Capping Layer (mm)']
data_ab = data_ab.dropna().reset_index(drop=True)

# --- Extract System C table (rows 13–18, columns A–E) ---
data_c = df.iloc[13:19, 0:5].copy()
data_c.columns = ['Loading Category', 'Block/Laying Course (mm)', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)', 'Capping Layer (mm)']
data_c = data_c.dropna().reset_index(drop=True)

# --- User Inputs ---
st.title("Permeable Paving Build-Up Tool")

system = st.selectbox("Select System", [
    "System A (full infiltration)",
    "System B (partial infiltration)",
    "System C (tanked)"
])

category = st.selectbox("Select Loading Category", [
    "A/domestic",
    "B/car parking",
    "C/pedestrian",
    "D/shopping",
    "E/commercial",
    "F/heavy traffic"
])

cbr_str = st.selectbox("Select CBR (%)", [
    "1%", "2%", "3%", "4%", "5%", "8%", "10%", "15%"
])
cbr_value = int(cbr_str.replace('%', ''))

st.markdown("---")

# --- Lookup Result ---
st.subheader("Build-up Results")

if "System C" in system:
    match = data_c[data_c["Loading Category"] == category]
else:
    match = data_ab[data_ab["Loading Category"] == category]

if not match.empty:
    row = match.iloc[0].copy()

    # Apply CBR logic
    if cbr_value < 5:
        if "System C" in system:
            cbr_to_capping = {1: 600, 2: 350, 3: 250, 4: 200}
            row['Capping Layer (mm)'] = cbr_to_capping.get(cbr_value, row['Capping Layer (mm)'])
        else:
            cbr_to_cgm_add = {1: 300, 2: 175, 3: 125, 4: 100}
            row['Coarse Graded Material (mm)'] += cbr_to_cgm_add.get(cbr_value, 0)

    # Display output
    st.write(f"**Block/Laying Course:** {row['Block/Laying Course (mm)']} mm")
    st.write(f"**Hydraulically Bound Base:** {row['Hydraulically Bound Base (mm)']} mm")
    st.write(f"**Coarse Graded Material:** {row['Coarse Graded Material (mm)']} mm")
    st.write(f"**Capping Layer:** {row['Capping Layer (mm)']} mm")
else:
    st.warning("No matching build-up found for the selected inputs.")
