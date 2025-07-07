
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel data
df = pd.read_excel("Paving Tool.xlsx", sheet_name="Sheet1", header=None)

# --- Extract System A/B table (rows 8–13, columns C–F) ---
data_ab = df.iloc[8:14, 2:6].copy()
data_ab.columns = ['Loading Category', 'Block/Laying Course (mm)', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)']
data_ab = data_ab.dropna().reset_index(drop=True)

# --- Extract System C table (rows 20–25, columns C–F) ---
data_c = df.iloc[20:26, 2:6].copy()
data_c.columns = ['Block/Laying Course (mm)', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)', 'Capping Layer (mm)']
# Manually add Loading Categories
data_c.insert(0, 'Loading Category', [
    "A/domestic",
    "B/car parking",
    "C/pedestrian",
    "D/shopping",
    "E/commercial",
    "F/heavy traffic"
])
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

cbr = st.selectbox("Select CBR (%)", [
    "1%", "2%", "3%", "4%", "5%", "8%", "10%", "15%"
])

st.markdown("---")

# --- Lookup Result ---
st.subheader("Build-up Results")

if "System C" in system:
    match = data_c[data_c["Loading Category"] == category]
else:
    match = data_ab[data_ab["Loading Category"] == category]

if not match.empty:
    row = match.iloc[0]

    st.write(f"**Block/Laying Course:** {row['Block/Laying Course (mm)']} mm")
    st.write(f"**Hydraulically Bound Base:** {row['Hydraulically Bound Base (mm)']} mm")
    st.write(f"**Coarse Graded Material:** {row['Coarse Graded Material (mm)']} mm")

    if "System C" in system:
        st.write(f"**Capping Layer:** {row['Capping Layer (mm)']} mm")

else:
    st.warning("No matching build-up found for the selected inputs.")
