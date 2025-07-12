import spidev  # Controls SPI communication, used to talk to the MCP3008 ADC chip 
import time  # Allows use of sleep and time-based operations
from gpiozero import OutputDevice  # For controlling relay on Raspberry Pi 5
import csv  # For writing sensor data to a CSV file
from datetime import datetime  # For timestamping

# Initialize SPI communication with MCP3008
spi = spidev.SpiDev()  # Create SPI object
spi.open(0, 0)  # Open SPI bus 0, device 0 (chip select 0)
spi.max_speed_hz = 1350000  # Set SPI speed to 1.35 MHz

# Initialize relay control on GPIO17 pin
relay = OutputDevice(17)  # Relay will be switched via GPIO17

# Function to read analog value (0–1023) from specified MCP3008 channel (0–7)
def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])  # Send 3-byte command to MCP3008
    data = ((adc[1] & 3) << 8) + adc[2]  # Combine response bytes into 10-bit value
    return data  # Return raw ADC reading

# Convert raw ADC value to voltage using 3.3V reference
def convert_to_voltage(data, vref=3.3):
    return (data * vref) / 1023.0  # Scale ADC value proportionally to voltage

# Calibration constants for ACS712 current sensor
ACS712_ZERO_CURRENT = 2.5  # Voltage at 0A (measured baseline)
ACS712_SENSITIVITY = 0.066  # Sensitivity in volts/amp (66mV/A for 30A module)

# Thresholds for hysteresis control logic
ON_THRESHOLD = 0.08  # Turn ON relay when current > 80mA
OFF_THRESHOLD = 0.04  # Turn OFF relay when current < 40mA
motor_on = False  # Tracks if motor is currently ON

# Baseline variables for detecting spikes and energy accumulation
prev_current = 0  # Previous current reading (for spike detection)
prev_voltage = 0  # Previous voltage reading (for fluctuation detection)
cumulative_energy = 0  # Accumulates energy consumption in Wh
prev_relay_state = False  # Tracks last relay state (for change detection)

print("Reading current and voltage...")  # Notify user that monitoring has started

# Open CSV file to log sensor data with new features
with open('sensor_log1.csv', mode='w', newline='') as file:
    writer = csv.writer(file)  # Create CSV writer
    writer.writerow([
        'Timestamp', 'Current Sensor Voltage (V)', 'Current (A)',
        'Voltage Sensor Output (V)', 'Relay State',
        'Power (W)', 'Cumulative Energy (Wh)', 'Relay Changed',
        'Current Spike', 'Voltage Fluctuation'
    ])  # Write header row to CSV

    try:
        while True:  # Continuously read, process, and log sensor data
            raw_current = read_channel(0)  # Read from channel 0 (ACS712)
            raw_voltage = read_channel(1)  # Read from channel 1 (ZMPT101B)

            voltage_current = convert_to_voltage(raw_current)  # Convert current sensor to voltage
            voltage_voltage = convert_to_voltage(raw_voltage)  # Convert voltage sensor to voltage
            current = (voltage_current - ACS712_ZERO_CURRENT) / ACS712_SENSITIVITY  # Convert voltage to current

            # Relay hysteresis logic
            if abs(current) > ON_THRESHOLD and not motor_on:
                relay.on()  # Turn on relay
                motor_on = True
            elif abs(current) < OFF_THRESHOLD and motor_on:
                relay.off()  # Turn off relay
                motor_on = False

            # Calculate power in watts (P = V × I)
            power = voltage_voltage * current
            # Increment cumulative energy in watt-hours (Wh = W × hr)
            cumulative_energy += (power * 1 / 3600)  # 1 second = 1/3600 hour

            # Track relay state and changes
            relay_state = 'ON' if motor_on else 'OFF'
            relay_changed = (motor_on != prev_relay_state)

            # Detect current spike (ΔCurrent > 0.1A)
            current_spike = abs(current - prev_current) > 0.1
            # Detect voltage fluctuation (ΔVoltage > 0.2V)
            voltage_fluctuation = abs(voltage_voltage - prev_voltage) > 0.2

            # Print live readings to console
            print(f"Current Sensor Voltage: {voltage_current:.2f} V → Current: {current:.2f} A")
            print(f"Voltage Sensor Output: {voltage_voltage:.2f} V")
            print("-" * 40)

            # Write all values and new features to CSV file
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            writer.writerow([
                timestamp, f"{voltage_current:.2f}", f"{current:.2f}",
                f"{voltage_voltage:.2f}", relay_state,
                f"{power:.2f}", f"{cumulative_energy:.4f}",
                relay_changed, current_spike, voltage_fluctuation
            ])
            file.flush()  # Force data to be written to file immediately

            # Update previous values for next iteration
            prev_current = current
            prev_voltage = voltage_voltage
            prev_relay_state = motor_on

            time.sleep(1)  # Wait 1 second before next reading

    except KeyboardInterrupt:  # If user stops script with Ctrl+C
        print("\nStopped by user.")  # Display exit message
    finally:
        spi.close()  # Close SPI connection safely on exit
