import streamlit as st

# --- App Title & Branding ---
st.set_page_config(page_title="PHAGA: Pharma-Grade Alcohol Optimizer", page_icon="🧪", layout="centered")

st.markdown("""
    <div style="background-color:#0d6efd;padding:10px;border-radius:10px">
    <h2 style="color:white;text-align:center;">PHAGA: Pharma-Grade Alcohol Best Parameters Based on Molasses Parameters by Elhussien</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h4 style='color:#0d6efd;text-align:center;'>Literature-backed optimization for ethanol production</h4>", unsafe_allow_html=True)

# --- Input Panel ---
st.header("🔹 Enter Molasses & Fermentation Data")

trs_input = st.number_input("Molasses TRS (%)", min_value=5.0, max_value=30.0, value=18.0, step=0.1)
fan_input = st.number_input("Molasses FAN (mg/L)", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
ph_input = st.number_input("Molasses pH", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
vol_input = st.number_input("Molasses Solution Volume (L)", min_value=10.0, max_value=50000.0, value=1000.0, step=10.0)
target_trs = st.number_input("Target TRS (g/L)", min_value=100.0, max_value=200.0, value=150.0, step=10.0)
temp_input = st.number_input("Fermentation Temp (°C)", min_value=25.0, max_value=35.0, value=30.0, step=0.5)

# --- Calculations ---
# Convert TRS% to g/L (assume density 1.0 kg/L)
trs_input_gl = trs_input * 10  # e.g. 18% -> 180 g/L
final_vol = vol_input * trs_input_gl / target_trs
water_needed = final_vol - vol_input

# FAN adjustment
target_fan = 220.0
needed_fan_mg = max(0.0, (target_fan - fan_input) * final_vol)
needed_fan_g = needed_fan_mg / 1000.0  # g N

# Convert to nitrogen salts
g_ammonium_sulfate = needed_fan_g / 0.21 if needed_fan_g > 0 else 0
g_urea = needed_fan_g / 0.46 if needed_fan_g > 0 else 0
g_dap = needed_fan_g / 0.18 if needed_fan_g > 0 else 0

# Yeast dosage
yeast_g_per_l = 0.27  # literature value
yeast_needed_g = final_vol * yeast_g_per_l

# --- Risk estimation ---
ipa_risk = "LOW"
methanol_risk = "LOW"
if temp_input > 32.0 or fan_input < 150:
    ipa_risk = "HIGH"
if trs_input_gl > 200.0 or ph_input > 5.2:
    methanol_risk = "HIGH"

# --- Results ---
st.header("✅ Recommended Parameters")

st.info(f"💧 **Add Water:** {water_needed:.1f} L to adjust sugar to {target_trs} g/L")

if needed_fan_g > 0:
    st.write("🌱 **Add Nitrogen Sources to meet FAN target (~220 mg/L):**")
    st.write(f"- Ammonium sulfate: **{g_ammonium_sulfate:.1f} g**")
    st.write(f"- Urea: **{g_urea:.1f} g**")
    st.write(f"- DAP: **{g_dap:.1f} g**")
else:
    st.success("🌱 FAN sufficient — no additional nitrogen needed.")

if ph_input < 4.5:
    st.warning("⚠️ pH is low — adjust upward to ~5.0")
elif ph_input > 5.0:
    st.warning("⚠️ pH is high — adjust downward to ~5.0")
else:
    st.success("✅ pH is in optimal range (~5.0)")

st.write(f"🦠 **Yeast required:** {yeast_needed_g:.1f} g dry yeast")

st.write(f"🌡️ **Maintain fermentation temp at:** {temp_input} °C")

st.header("🚨 By-product Risk")
st.write(f"🧪 **IPA risk:** {ipa_risk}")
st.write(f"🧪 **Methanol risk:** {methanol_risk}")

if ipa_risk == "HIGH":
    st.warning("🔑 Reduce temperature or increase FAN to lower IPA risk.")
if methanol_risk == "HIGH":
    st.warning("🔑 Dilute molasses or adjust pH to reduce methanol risk.")

st.success("PHAGA (literature-based) analysis complete. Apply adjustments before fermentation.")
