
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
    "1%", "2%", "3%", "4%", "5%", "8%", "10%", "15%"
])

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
        row["Coarse Graded Material (mm)"] += 300
    elif cbr == 2:
        row["Coarse Graded Material (mm)"] += 175
    elif cbr == 3:
        row["Coarse Graded Material (mm)"] += 125
    elif cbr == 4:
        row["Coarse Graded Material (mm)"] += 100
else:
    if cbr == 1:
        row["Capping Layer (mm)"] = 600
    elif cbr == 2:
        row["Capping Layer (mm)"] = 350
    elif cbr == 3:
        row["Capping Layer (mm)"] = 250
    elif cbr == 4:
        row["Capping Layer (mm)"] = 200

# Display results
st.subheader("Calculated Build-Up Thicknesses")
st.write(f"**Block/Laying Course:** {row['Block/Laying Course (mm)']} mm")
st.write(f"**Hydraulically Bound Base:** {row['Hydraulically Bound Base (mm)']} mm")
st.write(f"**Coarse Graded Material:** {row['Coarse Graded Material (mm)']} mm")
st.write(f"**Capping Layer:** {row['Capping Layer (mm)']} mm")

# New input: Area in square metres
area_m2 = st.number_input("Enter Area (m²)", min_value=0.0, format="%.2f")

# Calculate total thickness (sum of layers)
total_thickness_mm = (
    row['Block/Laying Course (mm)'] +
    row['Hydraulically Bound Base (mm)'] +
    row['Coarse Graded Material (mm)'] +
    row['Capping Layer (mm)']
)

# Calculate volume in cubic metres
volume_m3 = (area_m2 * total_thickness_mm) / 1000  # mm to m conversion

# Output volume
st.write(f"**Volume of Works:** {volume_m3:.2f} m³")

from PIL import Image

# Show the image below the results
image = Image.open("Image.png")
st.image(image, caption="Pavement Build-Up Diagram", use_container_width=True)
