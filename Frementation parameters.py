import streamlit as st

# --- App Config ---
st.set_page_config(
    page_title="PHAGA: Pharma-Grade Alcohol Optimizer (Lab Version)",
    page_icon="🧪",
    layout="centered"
)

# --- Header ---
st.markdown("""
    <div style="background-color:#0d6efd;padding:12px;border-radius:10px">
    <h2 style="color:white;text-align:center;">PHAGA: Pharma-Grade Alcohol Optimizer</h2>
    <h4 style="color:white;text-align:center;">Lab Version by Elhussien</h4>
    </div>
""", unsafe_allow_html=True)

st.header("🔬 Lab-Controlled Inputs")

# --- Inputs ---
trs_input = st.number_input("Molasses TRS (%) [5–50]", min_value=5.0, max_value=50.0, value=18.0, step=0.1)
fan_input = st.number_input("Molasses FAN (mg/L) [0–500]", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
ph_input = st.number_input("Molasses pH [7.0–8.0]", min_value=7.0, max_value=8.0, value=7.2, step=0.1)
target_trs = st.number_input("Target TRS after dilution (g/L) [110–140]", min_value=110.0, max_value=140.0, value=130.0, step=1.0)
temp_input = st.number_input("Fermentation Temp (°C) [25–35]", min_value=25.0, max_value=35.0, value=30.0, step=0.5)

mol_grade = st.selectbox("Molasses Grade", ["Clean", "Grade 1", "Grade 2", "Blackstrap"])
mol_density = st.number_input("Molasses Density (kg/L) [1.2–1.6]", min_value=1.2, max_value=1.6, value=1.4, step=0.01)

yeast_type = st.selectbox("Yeast Type (Lab Standard)", ["Sychrmiss-6"])

# --- Constants ---
fermentor_volume = 238000  # L
target_fan = 220.0  # mg/L

# --- Core Calculations ---
trs_input_gl = trs_input * 10  # to g/L
final_vol = fermentor_volume * trs_input_gl / target_trs
water_needed = final_vol - fermentor_volume

# --- FAN Calculation ---
needed_fan_mg = max(0.0, (target_fan - fan_input) * final_vol)
needed_fan_g = needed_fan_mg / 1000.0

g_ammonium_sulfate = needed_fan_g / 0.21 if needed_fan_g > 0 else 0
g_urea = needed_fan_g / 0.46 if needed_fan_g > 0 else 0
g_dap = needed_fan_g / 0.18 if needed_fan_g > 0 else 0

# --- Adjustments for Grade ---
base_yeast_gpl = 0.27
nutrient_factor = 1.0

if mol_grade == "Blackstrap":
    base_yeast_gpl *= 1.1
    nutrient_factor = 1.2
    target_trs = min(target_trs, 140)
elif mol_grade == "Grade 2":
    base_yeast_gpl *= 1.05
    nutrient_factor = 1.1

yeast_needed_g = final_vol * base_yeast_gpl
g_ammonium_sulfate *= nutrient_factor
g_urea *= nutrient_factor
g_dap *= nutrient_factor

# Convert all additives to kilograms
kg_ammonium_sulfate = g_ammonium_sulfate / 1000
kg_urea = g_urea / 1000
kg_dap = g_dap / 1000
yeast_needed_kg = yeast_needed_g / 1000

# --- Risk Estimation ---
ipa_risk = "LOW"
methanol_risk = "LOW"

if temp_input > 32.0 or fan_input < 150:
    ipa_risk = "HIGH"
if trs_input_gl > 200 or ph_input > 7.5 or mol_grade == "Blackstrap":
    methanol_risk = "HIGH"

# --- Output Section ---
st.header("✅ Recommended Parameters (Lab-Controlled)")

st.info(f"💧 Water to Add: **{water_needed:.1f} L** to reach {target_trs:.0f} g/L TRS")
st.write(f"🧬 Yeast Used: `{yeast_type}` — Required: **{yeast_needed_kg:.2f} kg**")
st.write(f"🌡️ Maintain Fermentation Temp: **{temp_input:.1f} °C**")
st.write(f"🧪 Molasses Grade: `{mol_grade}` — Density: **{mol_density:.2f} kg/L**")

# --- Nitrogen Recommendations ---
if needed_fan_g > 0:
    st.subheader("🌱 FAN Adjustment:")
    st.write(f"- Ammonium Sulfate: **{kg_ammonium_sulfate:.2f} kg**")
    st.write(f"- Urea: **{kg_urea:.2f} kg**")
    st.write(f"- DAP: **{kg_dap:.2f} kg**")
else:
    st.success("✅ FAN sufficient — no nitrogen additions needed.")

# --- Quality Warnings ---
if mol_grade in ["Grade 2", "Blackstrap"]:
    st.warning("⚠️ Use pretreatment (filter/settle) to reduce solids and methanol risk.")

# --- pH Status ---
if ph_input > 7.8:
    st.warning("⚠️ pH slightly high — aim for 7.0–7.5")
else:
    st.success("✅ pH within safe range for lab-controlled process.")

# --- Risk Display ---
st.header("🚨 Contaminant Risk")
st.write(f"🧪 IPA Risk: {ipa_risk}")
st.write(f"🧪 Methanol Risk: {methanol_risk}")

if ipa_risk == "HIGH":
    st.warning("🔑 IPA risk high — reduce temp or increase FAN.")
if methanol_risk == "HIGH":
    st.warning("🔑 Methanol risk high — dilute molasses or pre-clean low-grade feed.")

st.success("✅ PHAGA (Lab Version) analysis complete.")
