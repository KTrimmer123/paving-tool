import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(layout="wide")

# Load spreadsheet
df = pd.read_excel("Paving Tool UPDATED.xlsx")

# User inputs
paving_type = st.selectbox("Select paving type", df["Paving Type"].unique())
cb_value = st.selectbox("Select CBR value", df["CBR"].unique())
area_m2 = st.number_input("Enter Area (m²)", min_value=0.0, format="%.2f")

# Filter row
row = df[(df["Paving Type"] == paving_type) & (df["CBR"] == cb_value)].iloc[0]

# Show image
try:
    image = Image.open("Image.png")
    st.image(image, caption="Pavement Build-Up Diagram", use_container_width=True)
except Exception as e:
    st.error(f"Error loading image: {e}")

# Output thicknesses
st.subheader("Calculated Build-Up Thicknesses")
st.write(f"**Block/Laying Course:** 130 mm (fixed)")
st.write(f"**Hydraulically Bound Base:** {row['Hydraulically Bound Base (mm)']} mm")
st.write(f"**Coarse Graded Material:** {row['Coarse Graded Material (mm)']} mm")
st.write(f"**Capping Layer:** {row['Capping Layer (mm)']} mm")

if area_m2 > 0:
    try:
        # Fixed value for Block/Laying Course
        blc = 130
        hbb = float(row['Hydraulically Bound Base (mm)'])
        cgm = float(row['Coarse Graded Material (mm)'])
        cap = float(row['Capping Layer (mm)'])
        total_thickness_mm = blc + hbb + cgm + cap
        volume_m3 = (area_m2 * total_thickness_mm) / 1000
        st.write(f"**Volume of Works:** {volume_m3:.2f} m³")

        # Carbon Factors (kg CO₂e/m³)
        carbon_excavation = volume_m3 * 5
        carbon_cart = volume_m3 * 16

        st.markdown("### Carbon Estimates")
        st.write(f"**Excavation only:** {carbon_excavation:.0f} kg CO₂e ({carbon_excavation / 1000:.2f} tonnes)")
        st.write(f"**Excavation + cart-away:** {carbon_cart:.0f} kg CO₂e ({carbon_cart / 1000:.2f} tonnes)")
        st.caption("Based on average UK construction emissions factors per m³")

        # Build-up carbon estimates
        carbon_block_layer = 120    # kg CO₂e/m³ for 130mm fixed
        carbon_hbm = 45
        carbon_cga = 8
        carbon_capping = 5

        hbb_m = hbb / 1000
        cgm_m = cgm / 1000
        cap_m = cap / 1000

        block_vol = area_m2 * 0.13
        hbb_vol = area_m2 * hbb_m
        cgm_vol = area_m2 * cgm_m
        cap_vol = area_m2 * cap_m

        carbon_block = block_vol * carbon_block_layer
        carbon_hbb = hbb_vol * carbon_hbm
        carbon_cgm = cgm_vol * carbon_cga
        carbon_cap = cap_vol * carbon_capping
        total_material_carbon = carbon_block + carbon_hbb + carbon_cgm + carbon_cap

        st.markdown("### Build-Up Carbon Estimates")
        st.write(f"**Block + Bedding Sand:** {carbon_block:.0f} kg CO₂e ({carbon_block / 1000:.2f} tonnes)")
        st.write(f"**Hydraulically Bound Material:** {carbon_hbb:.0f} kg CO₂e ({carbon_hbb / 1000:.2f} tonnes)")
        st.write(f"**Coarse Graded Aggregate:** {carbon_cgm:.0f} kg CO₂e ({carbon_cgm / 1000:.2f} tonnes)")
        st.write(f"**Capping Layer:** {carbon_cap:.0f} kg CO₂e ({carbon_cap / 1000:.2f} tonnes)")
        st.write(f"**Total Build-Up Carbon:** {total_material_carbon:.0f} kg CO₂e ({total_material_carbon / 1000:.2f} tonnes)")
        st.caption("Based on standard UK embodied and installation carbon factors")

    except Exception as e:
        st.error(f"Error in volume calculation: {e}")