# Doppler Radar Based Vehicle Speed Estimation Using DSP

## 1. Project Overview

This project demonstrates vehicle speed estimation using the Doppler Radar principle and Digital Signal Processing (DSP).

A simulated Doppler radar signal is processed using Fast Fourier Transform (FFT) to identify its dominant frequency component. The Doppler frequency is then used to estimate the speed of a moving vehicle.

An interactive dashboard is developed using Python and Streamlit to visualise the radar signal, frequency spectrum, vehicle speed and detection results.

## 2. Objectives

* Understand the Doppler Effect in radar systems.
* Generate simulated Doppler radar signals.
* Apply FFT for frequency-domain analysis.
* Identify the dominant Doppler frequency.
* Estimate vehicle speed mathematically.
* Visualise the results through an interactive dashboard.

## 3. Technologies Used

* Python
* NumPy
* SciPy
* Matplotlib
* Streamlit
* Digital Signal Processing
* Fast Fourier Transform (FFT)

## 4. Working Principle

1. A radar signal is transmitted towards a moving vehicle.
2. The reflected signal experiences a frequency shift due to the Doppler Effect.
3. The received signal is processed using FFT.
4. The dominant frequency is extracted from the frequency spectrum.
5. Doppler frequency is converted into vehicle speed.
6. The estimated speed and signal characteristics are displayed on the dashboard.

## 5. Mathematical Equation

For a monostatic radar:

Doppler frequency:

fd = (2 * v * cos(theta)) / lambda

Vehicle speed:

v = (fd * lambda) / (2 * cos(theta))

Where:

* fd = Doppler frequency
* v = Vehicle velocity
* lambda = Radar wavelength
* theta = Angle between radar direction and vehicle motion

Radar wavelength:

lambda = c / fc

Where:

* c = Speed of light
* fc = Radar carrier frequency

## 6. Signal Processing

FFT is used to convert the received signal from the time domain into the frequency domain.

The dominant frequency component is identified to estimate the Doppler frequency.

## 7. Dashboard Features

* Interactive radar simulation
* Vehicle speed estimation
* Vehicle direction selection
* Radar angle calculation
* FFT frequency spectrum
* Dominant frequency identification
* Speed warning levels
* Signal visualisation

## 8. How to Run

Clone the repository:

git clone YOUR_REPOSITORY_URL

Navigate to the project directory:

cd Doppler-Radar-Vehicle-Speed-Estimation

Install dependencies:

pip install -r requirements.txt

Run the application:

streamlit run app(1).py

## 9. Disclaimer

This project is a software-based simulation demonstrating Doppler radar principles and DSP techniques. It does not represent measurements from a physical radar sensor.

## 10. Author

Arosh Rolly

B.Tech Electronics and Communication Engineering

Government Engineering College Thrissur
