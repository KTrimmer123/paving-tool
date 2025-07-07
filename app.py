
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load Excel data
df = pd.read_excel("Paving Tool.xlsx", sheet_name="Sheet1", header=None)

# Extract the System A/B data table (rows 8 to 13, columns 2–4)
data = df.iloc[8:14, 2:5]
data.columns = ['Loading Category', 'Hydraulically Bound Base (mm)', 'Coarse Graded Material (mm)']
data.insert(1, 'Block/Laying Course (mm)', '80/50')  # Fixed value

# Drop NaNs and clean
data = data.dropna().reset_index(drop=True)

# Convert numeric values
data['Hydraulically Bound Base (mm)'] = pd.to_numeric(data['Hydraulically Bound Base (mm)'], errors='coerce')
data['Coarse Graded Material (mm)'] = pd.to_numeric(data['Coarse Graded Material (mm)'], errors='coerce')

# UI
st.title("Permeable Paving Build-Up Tool")

st.markdown("### Select Build-up Parameters")
system = st.selectbox("System", ["System A or B (full/partial infiltration)"])
category = st.selectbox("Loading Category", data["Loading Category"].unique())

# Get the row matching the selected category
row = data[data["Loading Category"] == category].iloc[0]

# Display thickness info
st.subheader("Selected Build-up Thicknesses")
st.write(f"**Block/Laying Course:** {row['Block/Laying Course (mm)']} mm")
st.write(f"**Hydraulically Bound Base:** {int(row['Hydraulically Bound Base (mm)'])} mm")
st.write(f"**Coarse Graded Material:** {int(row['Coarse Graded Material (mm)'])} mm")

# Parse block/laying course into two layers
block_laying = row["Block/Laying Course (mm)"].split("/")
block_thickness = int(block_laying[0])
laying_course_thickness = int(block_laying[1])

# Prepare layers for plot
layers = [
    ("Block Pavers", block_thickness),
    ("Laying Course", laying_course_thickness),
    ("H.B. Base", int(row["Hydraulically Bound Base (mm)"])),
    ("CGM Sub-base", int(row["Coarse Graded Material (mm)"]))
]

# Plot build-up
fig, ax = plt.subplots(figsize=(3, 6))
bottom = 0
for label, height in reversed(layers):
    ax.bar(0, height, bottom=bottom, width=0.5, label=label)
    bottom += height

ax.set_ylim(0, bottom + 50)
ax.set_xlim(-1, 1)
ax.set_xticks([])
ax.set_ylabel("Depth (mm)")
ax.invert_yaxis()
ax.legend(loc='upper right')

st.pyplot(fig)
