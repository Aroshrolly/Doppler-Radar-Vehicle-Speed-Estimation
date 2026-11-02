import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import firwin, lfilter
from scipy.signal.windows import hamming

# ------------------------------------------------------------
# Doppler Radar Vehicle Speed Estimation Using DSP
# Streamlit dashboard version of the MATLAB/Colab simulation
# ------------------------------------------------------------

st.set_page_config(
    page_title="Doppler Radar Speed Estimation",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Doppler Radar Vehicle Speed Estimation Using DSP")
st.caption(
    "CW Doppler radar simulation: signal generation → noise → FIR filtering "
    "→ FFT peak detection → radial-speed estimation → angle correction."
)

# Original simulation parameters retained as defaults
c = 3e8
fc = 10.525e9
lambda_radar = c / fc
Fs = 10000
T = 2
NFFT = 16384
min_speed_kmh = 5
max_speed_kmh = 120
filterOrder = 100

# Sidebar controls
st.sidebar.header("Simulation Parameters")
actualSpeed_kmh = st.sidebar.slider(
    "Actual vehicle speed (km/h)", 5, 120, 70, 1
)
theta_deg = st.sidebar.slider(
    "Radar angle θ (degrees)", 0, 75, 30, 1
)
SNR_dB = st.sidebar.slider(
    "Signal-to-noise ratio (dB)", 0, 30, 10, 1
)
random_seed = st.sidebar.number_input(
    "Noise random seed", min_value=0, max_value=100000,
    value=0, step=1
)

st.sidebar.markdown("---")
st.sidebar.subheader("Warning thresholds")
yellow_limit = st.sidebar.number_input(
    "Green/Yellow threshold (km/h)", min_value=1, max_value=150,
    value=50, step=1
)
orange_limit = st.sidebar.number_input(
    "Yellow/Orange threshold (km/h)", min_value=1, max_value=180,
    value=60, step=1
)
red_limit = st.sidebar.number_input(
    "Orange/Red threshold (km/h)", min_value=1, max_value=200,
    value=80, step=1
)

# Derived values
t = np.arange(0, T, 1 / Fs)
N = len(t)
actualSpeed = actualSpeed_kmh / 3.6
theta = np.deg2rad(theta_deg)
radialSpeed = actualSpeed * np.cos(theta)
fd = 2 * radialSpeed / lambda_radar

# Synthetic Doppler signal + white Gaussian noise
dopplerSignal = np.sin(2 * np.pi * fd * t)
signalPower = np.mean(dopplerSignal ** 2)
noisePower = signalPower / (10 ** (SNR_dB / 10))
rng = np.random.default_rng(int(random_seed))
noise = np.sqrt(noisePower) * rng.standard_normal(N)
receivedSignal = dopplerSignal + noise

# FIR bandpass filter based on the original 5–120 km/h range
minFd = 2 * (min_speed_kmh / 3.6) / lambda_radar
maxFd = 2 * (max_speed_kmh / 3.6) / lambda_radar
Wn = [minFd, maxFd]

b = firwin(
    numtaps=filterOrder + 1,
    cutoff=Wn,
    window="hamming",
    pass_zero=False,
    fs=Fs
)
filteredSignal = lfilter(b, [1.0], receivedSignal)

# Window and FFT
window = hamming(N, sym=True)
windowedSignal = filteredSignal * window
Y = np.fft.fft(windowedSignal, n=NFFT)
P2 = np.abs(Y / N)
P1 = P2[:NFFT // 2 + 1].copy()
P1[1:-1] = 2 * P1[1:-1]
f = Fs * np.arange(NFFT // 2 + 1) / NFFT

# Detect strongest peak inside the configured Doppler band
valid_indices = np.where((f >= minFd) & (f <= maxFd))[0]
if len(valid_indices) == 0:
    st.error("No valid FFT frequency bins found. Check the sampling/filter settings.")
    st.stop()

indexPeak = valid_indices[np.argmax(P1[valid_indices])]
estimatedFd = f[indexPeak]
estimatedRadialSpeed = estimatedFd * lambda_radar / 2
estimatedRadialSpeed_kmh = estimatedRadialSpeed * 3.6

# Angle correction assumes the angle is known
cos_theta = np.cos(theta)
if abs(cos_theta) < 1e-9:
    estimatedSpeed_kmh = float("nan")
else:
    estimatedSpeed_kmh = estimatedRadialSpeed_kmh / cos_theta

estimatedSpeed = estimatedSpeed_kmh / 3.6
error_kmh = abs(actualSpeed_kmh - estimatedSpeed_kmh)
error_percent = (
    100 * error_kmh / actualSpeed_kmh if actualSpeed_kmh != 0 else 0
)

# Warning state
if estimatedSpeed_kmh <= yellow_limit:
    warning = "GREEN — SAFE"
    warning_color = "green"
elif estimatedSpeed_kmh <= orange_limit:
    warning = "YELLOW — CAUTION"
    warning_color = "orange"
elif estimatedSpeed_kmh <= red_limit:
    warning = "ORANGE — OVERSPEED"
    warning_color = "darkorange"
else:
    warning = "RED — DANGEROUS OVERSPEED"
    warning_color = "red"

# Top-level metric cards
st.subheader("Estimated Results")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Actual speed", f"{actualSpeed_kmh:.2f} km/h")
m2.metric("Radial speed (actual)", f"{radialSpeed * 3.6:.2f} km/h")
m3.metric("Estimated speed (corrected)", f"{estimatedSpeed_kmh:.2f} km/h")
m4.metric("Doppler frequency (actual)", f"{fd:.1f} Hz")

st.markdown(
    f"<div style='padding:14px;border-radius:10px;background:{warning_color};"
    f"color:white;font-size:22px;font-weight:700;text-align:center;'>"
    f"Speed Warning: {warning}</div>",
    unsafe_allow_html=True
)
st.write(
    f"**Estimated Doppler frequency:** {estimatedFd:.2f} Hz  |  "
    f"**Absolute error:** {error_kmh:.2f} km/h  |  "
    f"**Percentage error:** {error_percent:.2f}%"
)

st.info(
    "Angle correction uses the selected angle: v = vᵣ / cos(θ). "
    "A single-channel CW Doppler signal does not independently determine the angle. "
    "This is a synthetic educational simulation, not measured radar data."
)

# Plot 1: received and filtered signals
st.subheader("1. Time-Domain Signals")
fig1, ax = plt.subplots(figsize=(12, 4))
samples_to_plot = min(2000, N)
ax.plot(t[:samples_to_plot], receivedSignal[:samples_to_plot], label="Received signal", alpha=0.7)
ax.plot(t[:samples_to_plot], filteredSignal[:samples_to_plot], label="Filtered signal", linewidth=1.4)
ax.set_xlabel("Time (s)")
ax.set_ylabel("Amplitude")
ax.set_title("Received Signal and FIR-Filtered Signal (first 2000 samples)")
ax.grid(True, alpha=0.3)
ax.legend()
fig1.tight_layout()
st.pyplot(fig1)
plt.close(fig1)

# Plot 2: FFT spectrum
st.subheader("2. FFT Spectrum and Detected Doppler Peak")
fig2, ax = plt.subplots(figsize=(12, 4))
ax.plot(f, P1, linewidth=1)
ax.axvline(estimatedFd, linestyle="--", label=f"Detected peak: {estimatedFd:.2f} Hz")
ax.axvline(fd, linestyle=":", label=f"Theoretical Doppler: {fd:.2f} Hz")
ax.set_xlim(0, min(Fs / 2, maxFd * 1.25))
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Single-sided amplitude")
ax.set_title("FFT Magnitude Spectrum")
ax.grid(True, alpha=0.3)
ax.legend()
fig2.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# Plot 3: actual vs estimated speed
st.subheader("3. Actual vs Estimated Speed")
fig3, ax = plt.subplots(figsize=(7, 4))
labels = ["Actual speed", "Estimated corrected speed"]
values = [actualSpeed_kmh, estimatedSpeed_kmh]
bars = ax.bar(labels, values)
ax.set_ylabel("Speed (km/h)")
ax.set_title("Speed Estimation Comparison")
ax.grid(axis="y", alpha=0.3)
for bar, value in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f"{value:.2f}", ha="center", va="bottom")
fig3.tight_layout()
st.pyplot(fig3)
plt.close(fig3)

# Plot 4: angle effect
st.subheader("4. Effect of Radar Angle")
angles = np.arange(0, 81, 5)
radial_speeds = actualSpeed_kmh * np.cos(np.deg2rad(angles))
fig4, ax = plt.subplots(figsize=(10, 4))
ax.plot(angles, radial_speeds, marker="o", label="Measured radial component")
ax.axhline(actualSpeed_kmh, linestyle="--", label="True vehicle speed")
ax.axvline(theta_deg, linestyle=":", label=f"Selected angle: {theta_deg}°")
ax.set_xlabel("Angle θ (degrees)")
ax.set_ylabel("Speed component (km/h)")
ax.set_title("Radial Speed Falls as Radar Angle Increases")
ax.grid(True, alpha=0.3)
ax.legend()
fig4.tight_layout()
st.pyplot(fig4)
plt.close(fig4)

# Plot 5: warning thresholds
st.subheader("5. Speed Warning Levels")
fig5, ax = plt.subplots(figsize=(10, 4))
ax.barh(["Estimated vehicle speed"], [estimatedSpeed_kmh])
for threshold, label in [
    (yellow_limit, "Green/Yellow"),
    (orange_limit, "Yellow/Orange"),
    (red_limit, "Orange/Red")
]:
    ax.axvline(threshold, linestyle="--", label=f"{label}: {threshold} km/h")
ax.set_xlabel("Speed (km/h)")
ax.set_xlim(0, max(130, estimatedSpeed_kmh * 1.15))
ax.set_title("Estimated Speed Against Warning Thresholds")
ax.grid(axis="x", alpha=0.3)
ax.legend()
fig5.tight_layout()
st.pyplot(fig5)
plt.close(fig5)

with st.expander("Show simulation parameters and DSP details"):
    st.write({
        "Radar carrier frequency (Hz)": fc,
        "Speed of light (m/s)": c,
        "Wavelength (m)": lambda_radar,
        "Sampling frequency (Hz)": Fs,
        "Simulation duration (s)": T,
        "Number of samples": N,
        "FFT length": NFFT,
        "SNR (dB)": SNR_dB,
        "FIR filter order": filterOrder,
        "Minimum Doppler frequency (Hz)": minFd,
        "Maximum Doppler frequency (Hz)": maxFd,
        "Theoretical Doppler frequency (Hz)": fd,
        "Detected Doppler frequency (Hz)": estimatedFd,
        "Angle correction used": f"v = v_r / cos({theta_deg}°)"
    })

st.caption(
    "Note: The FIR filter uses a Hamming-window design. FFT-bin spacing and noise can cause "
    "small differences between actual and estimated speed. Warning thresholds are demonstration values."
)
