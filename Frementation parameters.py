import streamlit as st

# --- App Configuration ---
st.set_page_config(
    page_title="PHAGA: Pharma-Grade Alcohol Optimizer",
    page_icon="🧪",
    layout="centered"
)

# --- Title & Branding ---
st.markdown("""
    <div style="background-color:#0d6efd;padding:10px;border-radius:10px">
    <h2 style="color:white;text-align:center;">PHAGA: Pharma-Grade Alcohol Best Parameters Based on Molasses Parameters by Elhussien</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h4 style='color:#0d6efd;text-align:center;'>Literature-backed optimization for ethanol production</h4>", unsafe_allow_html=True)

# --- Info Box for Parameter Ranges ---
st.markdown("""
<div style='background-color:#e9f5ff;padding:10px;border-radius:10px'>
<b>ℹ️ Valid Input Ranges:</b><br>
- Molasses TRS: 5–25%<br>
- FAN (Free Amino Nitrogen): 0–500 mg/L<br>
- pH: 3.0–7.0 (optimum ~5.0)<br>
- Target TRS after dilution: 100–200 g/L<br>
- Temperature: 25–35 °C<br>
- Molasses Grade: Clean → Blackstrap (affects viscosity)<br>
- Yeast: Based on strain performance
</div>
""", unsafe_allow_html=True)

# --- Input Section ---
st.header("🔹 Enter Process Inputs")

trs_input = st.number_input("Molasses TRS (%)", min_value=5.0, max_value=25.0, value=18.0, step=0.1)
fan_input = st.number_input("Molasses FAN (mg/L)", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
ph_input = st.number_input("Molasses pH", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
target_trs = st.number_input("Target Fermentation TRS (g/L)", min_value=100.0, max_value=200.0, value=150.0, step=10.0)
temp_input = st.number_input("Fermentation Temperature (°C)", min_value=25.0, max_value=35.0, value=30.0, step=0.5)

mol_grade = st.selectbox("Molasses Grade", ["Clean", "Grade 1", "Grade 2", "Blackstrap"])
mol_density = st.number_input("Molasses Density (kg/L)", min_value=1.2, max_value=1.6, value=1.4, step=0.01)
yeast_type = st.text_input("Yeast Type", value="Sychrmiss-6")

# --- Fixed Fermentor Volume ---
fermentor_volume = 238000  # L

# --- Internal Calculations ---
trs_input_gl = trs_input * 10  # TRS in g/L
final_vol = fermentor_volume * trs_input_gl / target_trs
water_needed = final_vol - fermentor_volume

# --- FAN Requirements ---
target_fan = 220.0
needed_fan_mg = max(0.0, (target_fan - fan_input) * final_vol)
needed_fan_g = needed_fan_mg / 1000.0

g_ammonium_sulfate = needed_fan_g / 0.21 if needed_fan_g > 0 else 0
g_urea = needed_fan_g / 0.46 if needed_fan_g > 0 else 0
g_dap = needed_fan_g / 0.18 if needed_fan_g > 0 else 0

# --- Yeast Dosage (adjusted for grade) ---
base_yeast_gpl = 0.27  # base dosage
base_nutrient_factor = 1.0

if mol_grade == "Blackstrap":
    base_yeast_gpl *= 1.1
    base_nutrient_factor = 1.2
    target_trs = min(target_trs, 150)
elif mol_grade == "Grade 2":
    base_yeast_gpl *= 1.05
    base_nutrient_factor = 1.1

yeast_needed_g = final_vol * base_yeast_gpl
g_ammonium_sulfate *= base_nutrient_factor
g_urea *= base_nutrient_factor
g_dap *= base_nutrient_factor

# --- Risk Estimations ---
ipa_risk = "LOW"
methanol_risk = "LOW"

if temp_input > 32.0 or fan_input < 150:
    ipa_risk = "HIGH"
if trs_input_gl > 200 or ph_input > 5.2 or mol_grade == "Blackstrap":
    methanol_risk = "HIGH"

# --- Output Section ---
st.header("✅ Recommended Operational Parameters")

st.info(f"💧 **Water to Add:** {water_needed:.1f} L (to reach ~{target_trs} g/L TRS)")

st.write(f"🧬 **Yeast Type:** {yeast_type}")
st.write(f"🦠 **Dry Yeast Required:** {yeast_needed_g:.1f} g")
st.write(f"🌡️ **Maintain Fermentation Temp:** {temp_input} °C")

# --- Nitrogen Advice ---
if needed_fan_g > 0:
    st.write("🌱 **Nitrogen Sources (to reach FAN ~220 mg/L):**")
    st.write(f"- Ammonium sulfate: **{g_ammonium_sulfate:.1f} g**")
    st.write(f"- Urea: **{g_urea:.1f} g**")
    st.write(f"- DAP: **{g_dap:.1f} g**")
else:
    st.success("✅ FAN is sufficient — no nitrogen addition needed.")

# --- pH Warnings ---
if ph_input < 4.5:
    st.warning("⚠️ pH is low — raise to ~5.0 using base (e.g., NaOH).")
elif ph_input > 5.0:
    st.warning("⚠️ pH is high — reduce to ~5.0 using acid (e.g., H₂SO₄).")
else:
    st.success("✅ pH is optimal (~5.0)")

# --- Molasses Grade Notes ---
st.write(f"🧪 **Molasses Grade:** {mol_grade}")
st.write(f"🧪 **Density:** {mol_density} kg/L")

if mol_grade in ["Grade 2", "Blackstrap"]:
    st.warning("⚠️ Low-grade molasses — consider pre-filtration or decanting to reduce impurities and prevent methanol formation.")

# --- Risk Section ---
st.header("🚨 Risk Estimation")
st.write(f"🧪 **IPA Risk:** {ipa_risk}")
st.write(f"🧪 **Methanol Risk:** {methanol_risk}")

if ipa_risk == "HIGH":
    st.warning("🔑 Reduce fermentation temperature or increase FAN to minimize IPA risk.")
if methanol_risk == "HIGH":
    st.warning("🔑 Lower TRS, optimize pH, or pretreat molasses to reduce methanol formation.")

st.success("✅ PHAGA analysis complete. Follow the above guidelines to maximize ethanol yield and purity.")
