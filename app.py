
import streamlit as st
import pandas as pd

# Title
st.title("Permeable Paving Build-Up Tool")

# Load Excel data
excel_file = "Paving Tool.xlsx"
df = pd.read_excel(excel_file, sheet_name="Sheet1", skiprows=8)

# Assign correct column headers for 5-column layout
df.columns = [
    "Loading Category",
    "Block/Laying Course (mm)",
    "Hydraulically Bound Base (mm)",
    "Coarse Graded Material (mm)",
    "Capping Layer (mm)"
]

# Add system indicator based on row position
df["System"] = ["System A or B"] * 6 + ["System C"] * 6

# Inputs
system = st.selectbox("Select System", ["System A (full infiltration)", "System B (partial infiltration)", "System C (tanked)"])
load_category = st.selectbox("Select Loading Category", df["Loading Category"].unique())
cbr_value = st.selectbox("Select CBR Value", ["1%", "2%", "3%", "4%", "5%", "8%", "10%", "15%"])

# Map system input to internal name
if "System C" in system:
    system_key = "System C"
else:
    system_key = "System A or B"

# Filter matching row
filtered = df[(df["System"] == system_key) & (df["Loading Category"] == load_category)]
if filtered.empty:
    st.error("No matching configuration found.")
    st.stop()

result = filtered.iloc[0].copy()

# Apply CBR logic
cbr = int(cbr_value.strip('%'))
if system_key == "System A or B":
    if cbr == 1:
        result["Coarse Graded Material (mm)"] += 300
    elif cbr == 2:
        result["Coarse Graded Material (mm)"] += 175
    elif cbr == 3:
        result["Coarse Graded Material (mm)"] += 125
    elif cbr == 4:
        result["Coarse Graded Material (mm)"] += 100
else:
    if cbr == 1:
        result["Capping Layer (mm)"] = 600
    elif cbr == 2:
        result["Capping Layer (mm)"] = 350
    elif cbr == 3:
        result["Capping Layer (mm)"] = 250
    elif cbr == 4:
        result["Capping Layer (mm)"] = 200

# Display results
st.subheader("Calculated Build-Up Thicknesses")
st.write(f"**Block/Laying Course:** {result['Block/Laying Course (mm)']} mm")
st.write(f"**Hydraulically Bound Base:** {result['Hydraulically Bound Base (mm)']} mm")
st.write(f"**Coarse Graded Material:** {result['Coarse Graded Material (mm)']} mm")
st.write(f"**Capping Layer:** {result['Capping Layer (mm)']} mm")
