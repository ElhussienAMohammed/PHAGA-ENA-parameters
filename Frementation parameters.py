import streamlit as st

# --- App Title & Branding ---
st.set_page_config(page_title="PHAGA: Pharma-Grade Alcohol Optimizer", page_icon="🧪", layout="centered")

st.markdown("""
    <div style="background-color:#0d6efd;padding:10px;border-radius:10px">
    <h2 style="color:white;text-align:center;">PHAGA: Pharma-Grade Alcohol Best Parameters Based on Molasses Parameters by Elhussien</h2>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h4 style='color:#0d6efd;text-align:center;'>Your trusted tool for clean fermentation</h4>", unsafe_allow_html=True)

# --- Input Panel ---
st.header("🔹 Enter Molasses & Fermentation Data")

trs_input = st.number_input("Molasses TRS (%)", min_value=5.0, max_value=30.0, value=18.0, step=0.1)
fan_input = st.number_input("Molasses FAN (mg/L)", min_value=0.0, max_value=500.0, value=150.0, step=1.0)
ph_input = st.number_input("Molasses pH", min_value=3.0, max_value=7.0, value=5.0, step=0.1)
vol_input = st.number_input("Molasses Solution Volume (L)", min_value=10.0, max_value=50000.0, value=1000.0, step=10.0)
target_trs = st.number_input("Target TRS (%)", min_value=10.0, max_value=20.0, value=16.0, step=0.1)
yeast_pitch = st.number_input("Yeast Pitching Rate (% v/v)", min_value=5.0, max_value=15.0, value=10.0, step=0.1)
temp_input = st.number_input("Fermentation Temp (°C)", min_value=25.0, max_value=35.0, value=30.0, step=0.5)

# --- Calculations ---
final_vol = vol_input * trs_input / target_trs
water_needed = final_vol - vol_input
target_fan = 220.0
needed_n = max(0.0, (target_fan - fan_input) * final_vol / 1000.0)

g_ammonium_sulfate = needed_n / 0.21 if needed_n > 0 else 0
g_urea = needed_n / 0.46 if needed_n > 0 else 0
g_dap = needed_n / 0.18 if needed_n > 0 else 0

yeast_slurry = final_vol * yeast_pitch / 100.0

# --- By-product risk ---
ipa_risk = "LOW"
methanol_risk = "LOW"
if temp_input > 32.0 or fan_input < 150:
    ipa_risk = "HIGH"
if trs_input > 20.0 or ph_input > 5.2:
    methanol_risk = "HIGH"

# --- Results ---
st.header("✅ Recommended Parameters")

st.info(f"💧 **Add Water:** {water_needed:.1f} L to adjust TRS to {target_trs}%")

if needed_n > 0:
    st.write("🌱 **Add Nitrogen Sources:**")
    st.write(f"- Ammonium sulfate: **{g_ammonium_sulfate:.1f} g**")
    st.write(f"- Urea: **{g_urea:.1f} g**")
    st.write(f"- DAP: **{g_dap:.1f} g**")
else:
    st.success("🌱 FAN sufficient — no additional nitrogen needed.")

if ph_input < 4.5:
    st.warning("⚠️ pH is low — add base to adjust to 4.5-5.0")
elif ph_input > 5.0:
    st.warning("⚠️ pH is high — add acid to adjust to 4.5-5.0")
else:
    st.success("✅ pH is in optimal range.")

st.write(f"🦠 **Yeast slurry to add:** {yeast_slurry:.1f} L at {yeast_pitch}% v/v")
st.write(f"🌡️ **Maintain fermentation temp at:** {temp_input} °C")

st.header("🚨 By-product Risk")
st.write(f"🧪 **IPA risk:** {ipa_risk}")
st.write(f"🧪 **Methanol risk:** {methanol_risk}")

if ipa_risk == "HIGH":
    st.warning("🔑 Reduce temperature or improve FAN to lower IPA risk.")
if methanol_risk == "HIGH":
    st.warning("🔑 Dilute molasses (lower TRS) or adjust pH to reduce methanol risk.")

st.success("PHAGA analysis complete. Apply adjustments before starting fermentation.")
