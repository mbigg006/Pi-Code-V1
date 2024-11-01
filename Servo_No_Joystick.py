import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize I2C bus
i2c = busio.I2C(SCL, SDA)

# Initialize PCA9685 at default address 0x40
pca = PCA9685(i2c)
pca.frequency = 50  # Set frequency to 50Hz for servos

# Helper function to convert angle to pulse width
def angle_to_pwm(angle):
    min_pulse = 500  # Minimum pulse width in microseconds for 0 degrees
    max_pulse = 2500  # Maximum pulse width in microseconds for 180 degrees
    pulse_range = max_pulse - min_pulse
    angle_range = 180
    pulse_width = min_pulse + (pulse_range * angle / angle_range)
    duty_cycle = int(pulse_width / 20000 * 0xFFFF)  # Convert to 16-bit duty cycle
    return duty_cycle

# Define servo channels (adjust channels to match your setup)
servo_channels = [0, 1, 2, 3, 4, 5]  # Channels for each of the six servos

# Set all servos to 0 degrees
for channel in servo_channels:
    pca.channels[channel].duty_cycle = angle_to_pwm(0)
    print(f"Servo on channel {channel} set to 0 degrees")
time.sleep(2)  # Hold at 0 degrees for 2 seconds

# Sweep all servos from 0 to 180 degrees to test movement
for angle in range(0, 181, 10):  # Increment by 10 degrees
    for channel in servo_channels:
        pca.channels[channel].duty_cycle = angle_to_pwm(angle)
        print(f"Setting servo on channel {channel} to {angle} degrees")
    time.sleep(0.5)  # Delay between angle updates

# Return all servos to 0 degrees
for channel in servo_channels:
    pca.channels[channel].duty_cycle = angle_to_pwm(0)
    print(f"Servo on channel {channel} returned to 0 degrees")

# Cleanup
pca.deinit()
print("Test complete")
