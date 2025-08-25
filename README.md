# ⚡ Smart Energy Meter with Real-Time Anomaly Detection

A Raspberry Pi-based real-time current and voltage monitoring system using the ACS712 and ZMPT101B sensors. It logs power usage, detects anomalies, and controls a relay intelligently. This project is part of a signal processing and AI pipeline intended for smart energy analysis.

---

## 📌 Overview

This project was developed as part of my personal learning and engineering development using signal processing, embedded systems, and basic AI ideas. It captures voltage and current data from sensors, logs it into a CSV, and allows further analysis in MATLAB for pattern recognition, filtering, and anomaly detection.

---

## 🚀 Project Objectives

- ✅ Read analog signals from ACS712 (current sensor) and ZMPT101B (voltage sensor)
- ✅ Control a relay based on real-time current thresholds
- ✅ Log the following features in a CSV file:
  - Timestamp
  - Voltage
  - Current
  - Power (W)
  - Cumulative Energy (Wh)
  - Relay State & Relay Changed flag
  - Current Spikes & Voltage Fluctuations
- ✅ Analyze data in MATLAB for signal processing and ML
- 🧠 Future: Train ML models for event classification or anomaly detection (TensorFlow Lite)

---

## 📸 Hardware Used

- Raspberry Pi 5 (8GB RAM)
- ACS712 Current Sensor (30A)
- ZMPT101B Voltage Sensor
- 5V Relay Module
- MCP3008 ADC (for analog-to-digital conversion)
- LED / Motor for load testing
- 1N4007 Diode (1N40071,1N4002 - 1N4007 Diode work it doesn't matter)
- 220 ohm resistor (for LED 330 ohm resistor should also be fine)
- Multimeter (for calibration and measurement OPTIONAL)
- Jumper wires, breadboard, etc.

---
## Final Schematic
<img src="Work/SmartEnergy_Schematic.png" width="900">
---
## 🧠 Technologies Used

- Python 3
- CSV for data logging
- `gpiozero`, `spidev` libraries for GPIO and SPI
- MATLAB (for signal processing and ML prototyping)
- Fritzing (for circuit schematics)

---

## 📦 Installation (on Raspberry Pi OS)

Run these commands:

```bash

sudo apt update
sudo apt install python3-pip -y

pip3 install gpiozero spidev
