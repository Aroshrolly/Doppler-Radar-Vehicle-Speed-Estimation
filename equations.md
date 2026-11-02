# Mathematical Equations – Doppler Radar Vehicle Speed Estimation Using DSP

## 1. Doppler Effect Principle

The Doppler Effect is the change in frequency of a wave due to relative motion between the source and the observer.

In a radar system, when a transmitted electromagnetic wave strikes a moving vehicle, the reflected wave experiences a frequency shift.

* Approaching vehicle: Received frequency increases.
* Receding vehicle: Received frequency decreases.

For a monostatic radar (same antenna for transmission and reception), the Doppler frequency is:

**fd = (2 × v × cos(θ)) / λ**

Where:

* fd = Doppler frequency (Hz)
* v = Vehicle velocity (m/s)
* θ = Angle between radar line of sight and vehicle motion
* λ = Radar wavelength (m)

The factor 2 occurs because the radar wave travels from the radar to the vehicle and back.

---

## 2. Calculation of Radar Wavelength

The wavelength of the transmitted radar signal is calculated using:

**λ = c / fc**

Where:

* c = Speed of light = 3 × 10⁸ m/s
* fc = Radar carrier frequency (Hz)

Substituting this into the Doppler equation:

**fd = (2 × v × fc × cos(θ)) / c**

---

## 3. Vehicle Speed Calculation

Rearranging the Doppler equation:

**v = (fd × λ) / (2 × cos(θ))**

Since:

**λ = c / fc**

The velocity becomes:

**v = (fd × c) / (2 × fc × cos(θ))**

This gives the vehicle velocity in metres per second (m/s).

### Conversion into km/h

**V(km/h) = v × 3.6**

Therefore:

**V(km/h) = (fd × λ × 3.6) / (2 × cos(θ))**

---

## 4. Radar Signal Generation

In the simulation, a Doppler signal can be represented as a sinusoidal signal.

**x(t) = A × cos(2π × fd × t + φ)**

Where:

* A = Signal amplitude
* fd = Doppler frequency (Hz)
* t = Time (seconds)
* φ = Initial phase (radians)

For discrete-time signal generation:

**x[n] = A × cos(2π × fd × n / fs + φ)**

Where:

* n = Sample index
* fs = Sampling frequency (Hz)

If noise is included:

**x[n] = A × cos(2π × fd × n / fs + φ) + w[n]**

Here, w[n] represents simulated noise.

---

## 5. Sampling Frequency

The sampling frequency determines how many samples are taken per second.

**fs = 1 / Ts**

Where:

* fs = Sampling frequency (Hz)
* Ts = Sampling interval (seconds)

According to the Nyquist sampling theorem:

**fs > 2 × fmax**

The sampling frequency must be greater than twice the maximum frequency component to avoid aliasing.

---

## 6. Fast Fourier Transform (FFT)

FFT converts a signal from the time domain into the frequency domain.

The Discrete Fourier Transform (DFT) is mathematically expressed as:

**X[k] = Σ x[n] × e^(-j2πkn/N)**

Where:

* X[k] = Frequency-domain representation
* x[n] = Input signal
* N = Number of samples
* k = Frequency index
* j = Square root of -1
* n = Sample index

The summation is performed for n = 0 to N-1.

FFT is an efficient algorithm used to calculate the DFT.

### Magnitude Spectrum

The magnitude of the FFT is:

**|X[k]| = √(Re(X[k])² + Im(X[k])²)**

Where:

* Re(X[k]) = Real component
* Im(X[k]) = Imaginary component

The magnitude spectrum represents the strength of different frequency components.

---

## 7. Frequency Bin Calculation

The frequency corresponding to each FFT bin is:

**f[k] = (k × fs) / N**

Where:

* f[k] = Frequency of the kth FFT bin (Hz)
* fs = Sampling frequency (Hz)
* N = Number of FFT samples
* k = FFT bin index

### Frequency Resolution

**Δf = fs / N**

Where:

* Δf = Frequency resolution (Hz)
* fs = Sampling frequency (Hz)
* N = Number of FFT samples

Increasing the number of samples improves frequency resolution, provided the sampling frequency remains constant.

---

## 8. Dominant Frequency Extraction

The dominant frequency is the frequency component having the maximum magnitude in the FFT spectrum.

**k_max = argmax |X[k]|**

In simple words:

k_max = Index of the maximum value in the FFT magnitude spectrum.

The corresponding dominant frequency is:

**fd = (k_max × fs) / N**

For a real-valued signal, a one-sided spectrum is commonly used to analyse positive frequencies.

The DC component (0 Hz) should generally be excluded when identifying the Doppler frequency.

---

## 9. Angle Correction

The radar measures only the component of vehicle velocity along its line of sight.

The radial velocity is:

**vr = v × cos(θ)**

Therefore:

**v = vr / cos(θ)**

Combining this with the Doppler equation:

**v = (fd × λ) / (2 × cos(θ))**

Angle correction is important because the measured Doppler frequency decreases as the vehicle moves at an angle relative to the radar.

### Example

At θ = 0°:

cos(0°) = 1

The radar measures the full velocity component.

At θ = 60°:

cos(60°) = 0.5

Only half of the actual velocity is along the radar line of sight.

Note: As the angle approaches 90°, the Doppler-based speed estimate becomes increasingly sensitive to measurement errors.

---

## 10. Vehicle Direction

The Doppler frequency shift has a sign depending on whether the vehicle approaches or moves away from the radar.

Using a convention where approaching velocity is positive:

**fd_signed = (2 × v × cos(θ)) / λ**

For an approaching vehicle:

**fd_signed > 0**

For a receding vehicle:

**fd_signed < 0**

The speed magnitude is calculated using:

**v = (|fd_signed| × λ) / (2 × |cos(θ)|)**

Important:

A magnitude-only FFT cannot independently distinguish approaching and receding vehicles. Direction requires signed Doppler information, such as quadrature I/Q processing, or an externally supplied direction selection.

---

## 11. Complete Speed Estimation Process

The overall calculation follows these steps:

1. Generate or receive the Doppler radar signal.
2. Sample the signal at the selected sampling frequency.
3. Apply FFT to convert the signal into the frequency domain.
4. Calculate the magnitude spectrum.
5. Identify the dominant Doppler frequency.
6. Calculate the radar wavelength.
7. Apply the angle correction.
8. Calculate vehicle speed in m/s.
9. Convert the result into km/h.
10. Display the estimated speed and warning status.

### Overall Mathematical Expression

**V(km/h) = (|fd| × c × 3.6) / (2 × fc × |cos(θ)|)**

---

## 12. Speed Warning Classification

The estimated vehicle speed can be compared against a selected speed threshold.

Let:

* V = Estimated vehicle speed (km/h)
* V_limit = Selected speed limit (km/h)

The classification is:

**If V ≤ V_limit: Status = Normal**

**If V > V_limit: Status = Warning**

The simulation can use different warning levels depending on the selected speed ranges.

---

## 13. Software Implementation

The following Python functions are commonly used to implement the mathematical operations:

| Operation                   | Python Function             |
| --------------------------- | --------------------------- |
| Signal generation           | `np.cos()`                  |
| Time samples                | `np.arange()`               |
| FFT calculation             | `np.fft.fft()`              |
| FFT frequencies             | `np.fft.fftfreq()`          |
| Magnitude spectrum          | `np.abs()`                  |
| Maximum frequency component | `np.argmax()`               |
| Wavelength calculation      | `c / fc`                    |
| Angle conversion            | `np.cos(np.radians(theta))` |
| Speed conversion            | `speed * 3.6`               |
| Dashboard                   | `streamlit`                 |

---

## 14. Conclusion

The project demonstrates how the Doppler Effect can be combined with Digital Signal Processing to estimate the speed of moving vehicles.

FFT is used to extract the dominant Doppler frequency, while mathematical equations convert this frequency into vehicle speed.

Angle correction improves the speed estimation by considering the orientation of the vehicle relative to the radar.

The project provides an interactive software simulation of Doppler radar-based vehicle speed measurement.

---

**Note:** This project is a software-based simulation demonstrating Doppler radar principles and DSP techniques. It does not represent measurements from a physical radar sensor.
