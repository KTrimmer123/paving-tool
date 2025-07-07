
import streamlit as st
import pandas as pd
from PIL import Image

# Load images
image_ab = Image.open("System A or B.png")
image_c = Image.open("System C.png")

# Set page config
st.set_page_config(page_title="Permeable Paving Build-Up Tool", layout="centered")

st.title("Permeable Paving Build-Up Tool")

# Load Excel file
excel_file = "Paving Tool UPDATED.xlsx"

# User inputs
system = st.selectbox("Select System", ["System A (Full Infiltration)", "System B (Partial Infiltration)", "System C (Attenuation Only)"])
category = st.selectbox("Select Loading Category", ["A/domestic", "B/car parking", "C/pedestrian", "D/shopping", "E/commercial", "F/heavy traffic"])
cbr = st.selectbox("Select CBR (%)", ["1%", "2%", "3%", "4%", "5%", "8%", "10%", "15%"])

# Convert CBR to int for logic
cbr_value = int(cbr.strip('%'))

# Choose sheet based on system
if "System C" in system:
    sheet_name = "System C"
else:
    sheet_name = "System A or B"

# Lookup row based on category
row_map = {
    "A/domestic": 0,
    "B/car parking": 1,
    "C/pedestrian": 2,
    "D/shopping": 3,
    "E/commercial": 4,
    "F/heavy traffic": 5,
}

# Read relevant section of Excel
df = pd.read_excel(excel_file, sheet_name=sheet_name, skiprows=8, nrows=6)
df.columns = ['Loading Category', 'Block/Laying Course (mm)', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)', 'Capping Layer (mm)']

row = df.iloc[row_map[category]].copy()

# Apply CBR logic
if "System C" in system:
    if cbr_value == 1:
        row['Capping Layer (mm)'] = 600
    elif cbr_value == 2:
        row['Capping Layer (mm)'] = 350
    elif cbr_value == 3:
        row['Capping Layer (mm)'] = 250
    elif cbr_value == 4:
        row['Capping Layer (mm)'] = 200
else:
    if cbr_value == 1:
        row['Coarse Graded Material (mm)'] += 300
    elif cbr_value == 2:
        row['Coarse Graded Material (mm)'] += 175
    elif cbr_value == 3:
        row['Coarse Graded Material (mm)'] += 125
    elif cbr_value == 4:
        row['Coarse Graded Material (mm)'] += 100

# Display results
st.subheader("Recommended Build-Up:")
st.write(f"**Block/Laying Course:** {row['Block/Laying Course (mm)']} mm")
st.write(f"**Hydraulically Bound Base:** {row['Hydraulically Bound Base (mm)']} mm")
st.write(f"**Coarse Graded Material:** {row['Coarse Graded Material (mm)']} mm")
st.write(f"**Capping Layer:** {row['Capping Layer (mm)']} mm")

# Display image
if "System C" in system:
    st.image(image_c, caption="Typical Build-Up for System C", use_column_width=True)
else:
    st.image(image_ab, caption="Typical Build-Up for System A or B", use_column_width=True)
