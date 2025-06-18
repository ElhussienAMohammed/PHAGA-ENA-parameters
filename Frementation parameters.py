import streamlit as st

# --- Streamlit Config ---
st.set_page_config(
    page_title="PHAGA: Pharma-Grade Alcohol Optimizer",
    page_icon="🧪",
    layout="centered"
)

# --- Title and Header ---
st.markdown("""
    <div style="background-color:#0d6efd;padding:12px;border-radius:10px">
    <h2 style="color:white;text-align:center;">PHAGA: Pharma-Grade Alcohol Best Parameters Based on Molasses Parameters</h2>
    <h4 style="color:white;text-align:center;">By Elhussien</h4>
    </div>
""", unsafe_allow_html=True)

# --- Input Panel ---
st.header("🔹 Enter Molasses & Fermentation Inputs")

trs_input = st.number_input("Molasses TRS (%) [5–50]", min_value=5.0, max_value=50.0, value=18.0, step=0.1)
fan_input = st.number_input("FAN (mg/L) [0–500]", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
ph_input = st.number_input("Molasses pH [3.0–7.0]", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
target_trs = st.number_input("Target TRS after dilution (g/L) [100–200]", min_value=100.0, max_value=200.0, value=150.0, step=10.0)
temp_input = st.number_input("Fermentation Temp (°C) [25–35]", min_value=25.0, max_value=35.0, value=30.0, step=0.5)

mol_grade = st.selectbox("Molasses Grade (affects impurities/viscosity)", ["Clean", "Grade 1", "Grade 2", "Blackstrap"])
mol_density = st.number_input("Molasses Density (kg/L) [1.2–1.6]", min_value=1.2, max_value=1.6, value=1.4, step=0.01)

yeast_type = st.selectbox(
    "Yeast Type",
    ["Sychrmiss-6", "Safethanol GR-2", "Fermivin", "Turbo-Yeast", "Angel Alcohol Yeast", "Other"]
)

# --- Constants ---
fermentor_volume = 238000  # in Liters
target_fan = 220.0  # mg/L

# --- Calculations ---
trs_input_gl = trs_input * 10  # convert TRS % to g/L
final_vol = fermentor_volume * trs_input_gl / target_trs
water_needed = final_vol - fermentor_volume

# FAN Deficiency
needed_fan_mg = max(0.0, (target_fan - fan_input) * final_vol)
needed_fan_g = needed_fan_mg / 1000.0

g_ammonium_sulfate = needed_fan_g / 0.21 if needed_fan_g > 0 else 0
g_urea = needed_fan_g / 0.46 if needed_fan_g > 0 else 0
g_dap = needed_fan_g / 0.18 if needed_fan_g > 0 else 0

# Yeast dosage and nutrient adjustment
base_yeast_gpl = 0.27
nutrient_factor = 1.0

if mol_grade == "Blackstrap":
    base_yeast_gpl *= 1.1
    nutrient_factor = 1.2
    target_trs = min(target_trs, 150)
elif mol_grade == "Grade 2":
    base_yeast_gpl *= 1.05
    nutrient_factor = 1.1

yeast_needed_g = final_vol * base_yeast_gpl
g_ammonium_sulfate *= nutrient_factor
g_urea *= nutrient_factor
g_dap *= nutrient_factor

# --- Risk Evaluation ---
ipa_risk = "LOW"
methanol_risk = "LOW"

if temp_input > 32.0 or fan_input < 150:
    ipa_risk = "HIGH"
if trs_input_gl > 200 or ph_input > 5.2 or mol_grade == "Blackstrap":
    methanol_risk = "HIGH"

# --- Results Section ---
st.header("✅ Optimized Operational Parameters")

st.info(f"💧 **Add Water:** {water_needed:.1f} L to reach target TRS of {target_trs} g/L")

st.write(f"🧬 **Selected Yeast Type:** `{yeast_type}`")
st.write(f"🦠 **Dry Yeast Required:** **{yeast_needed_g:.1f} g**")
st.write(f"🌡️ **Maintain Temp:** **{temp_input} °C**")
st.write(f"🧪 **Molasses Grade:** {mol_grade}  —  **Density:** {mol_density} kg/L")

# --- FAN Recommendations ---
if needed_fan_g > 0:
    st.subheader("🌱 FAN Adjustment (Target = 220 mg/L):")
    st.write(f"- Ammonium sulfate: **{g_ammonium_sulfate:.1f} g**")
    st.write(f"- Urea: **{g_urea:.1f} g**")
    st.write(f"- DAP: **{g_dap:.1f} g**")
else:
    st.success("✅ FAN level is sufficient — no nitrogen needed.")

# --- pH Check ---
if ph_input < 4.5:
    st.warning("⚠️ pH is too low — adjust upward to ~5.0")
elif ph_input > 5.0:
    st.warning("⚠️ pH is too high — adjust downward to ~5.0")
else:
    st.success("✅ pH is optimal (~5.0)")

# --- Quality Warnings ---
if mol_grade in ["Grade 2", "Blackstrap"]:
    st.warning("⚠️ Impure molasses — consider filtration or decanting to avoid foaming, methanol, and off-flavors.")

# --- Risk Display ---
st.header("🚨 Contaminant Risk Estimation")
st.write(f"🧪 **IPA Risk:** {ipa_risk}")
st.write(f"🧪 **Methanol Risk:** {methanol_risk}")

if ipa_risk == "HIGH":
    st.warning("🔑 IPA risk high — lower temperature or increase FAN.")
if methanol_risk == "HIGH":
    st.warning("🔑 Methanol risk high — dilute more or pretreat low-grade molasses.")

st.success("🎯 PHAGA analysis complete. Apply the above parameters to achieve high-purity ethanol.")
