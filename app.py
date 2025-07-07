
import streamlit as st
import pandas as pd

# Load data
excel_file = "Paving Tool UPDATED.xlsx"
ab_df = pd.read_excel(excel_file, sheet_name=0, skiprows=9, nrows=6)
c_df = pd.read_excel(excel_file, sheet_name=0, skiprows=19, nrows=6)

ab_df["System"] = "System A or B"
c_df["System"] = "System C"

df = pd.concat([ab_df, c_df], ignore_index=True)
df.rename(columns={df.columns[0]: "Loading Category"}, inplace=True)

# User inputs
system = st.selectbox("Select System", [
    "System A (Full Infiltration)",
    "System B (Partial Infiltration)",
    "System C (Attenuation Only)"
])
loading_category = st.selectbox("Select Loading Category", [
    "A/domestic", "B/car parking", "C/pedestrian", 
    "D/shopping", "E/commercial", "F/heavy traffic"
])

cbr_value = st.selectbox("Select CBR Value", [
# Area input (in m²)
# Area input (in m²)
# Internal logic for filtering
system_lookup = "System C" if "System C" in system else "System A or B"
cbr = int(cbr_value.strip('%'))

row = df[(df["System"] == system_lookup) & (df["Loading Category"] == loading_category)]

if row.empty:
    st.error("No matching configuration found.")
    st.stop()

row = row.iloc[0].copy()

# Apply CBR logic
if system_lookup == "System A or B":
    if cbr == 1:
# Display results
st.subheader("Calculated Build-Up Thicknesses")
# New input: Area in square metres
# Calculate total thickness (sum of layers)
# Calculate volume in cubic metres
# Output volume
from PIL import Image

# Show the image below the results
image = Image.open("Image.png")
st.image(image, caption="Pavement Build-Up Diagram", use_container_width=True)

# Input: Area in square metres
# Compute total thickness
# Convert to cubic metres

# Display output

# Volume calculation
# Volume calculation

# Volume calculation

# Volume calculation

# Volume calculation

# Volume calculation
if area_m2 > 0:
    total_thickness_mm = (
        row['Block/Laying Course (mm)'] +
        row['Hydraulically Bound Base (mm)'] +
        row['Coarse Graded Material (mm)'] +
        row['Capping Layer (mm)']
    )
    volume_m3 = (area_m2 * total_thickness_mm) / 1000
    st.subheader("Volume Calculation")
    st.write(f"**Volume of Works:** {volume_m3:.2f} m³")
