import time
from adafruit_pca9685 import PCA9685
from board import SCL, SDA
import busio

# Initialize I2C and PCA9685 for servo control
i2c = busio.I2C(SCL, SDA)
pca = PCA9685(i2c)
pca.frequency = 50  # Standard frequency for servos

# Configuration for servos
SERVO_MIN = 150  # Minimum pulse length
SERVO_MAX = 600  # Maximum pulse length
NUM_SERVOS = 6   # Number of servos for 6-DOF arm

# Define initial positions for each servo as percentages (0 to 100)
# You can adjust these values as needed to control each DOF of the arm
servo_positions = [50, 75, 25, 50, 90, 10]  # Example positions in percentage

# Function to map a percentage value (0 to 100) to the servo pulse width
def map_position_to_servo(pct, min_pulse, max_pulse):
    """
    Maps a percentage value (0 to 100) to a pulse width within the servo's range.
    :param pct: Percentage value (0 to 100) for the servo position.
    :param min_pulse: Minimum pulse width for the servo.
    :param max_pulse: Maximum pulse width for the servo.
    :return: Corresponding pulse width for the given position.
    """
    return int((pct / 100) * (max_pulse - min_pulse) + min_pulse)

# Function to set servo positions
def set_servo_positions(positions):
    """
    Sets each servo to the specified position in `positions`.
    :param positions: List of percentage values (0 to 100) for each servo.
    """
    for i, pct in enumerate(positions):
        servo_pulse = map_position_to_servo(pct, SERVO_MIN, SERVO_MAX)
        pca.channels[i].duty_cycle = servo_pulse
        print(f"Setting Servo {i+1} to {pct}% -> Pulse {servo_pulse}")
    print("All servos set to specified positions.")

# Main program loop (example of moving through different positions)
try:
    while True:
        # Set servos to initial positions
        set_servo_positions(servo_positions)

        # Delay to hold position
        time.sleep(2)

        # Example of moving servos to a different position
        new_positions = [10, 50, 75, 30, 60, 90]
        print("Moving to new positions...")
        set_servo_positions(new_positions) 

        # Delay to hold new position
        time.sleep(2)

        # Move back to the initial positions
        print("Returning to initial positions...")
        set_servo_positions(servo_positions)

        # Delay to hold initial position
        time.sleep(2)

except KeyboardInterrupt:
    print("\nExiting...")

# Cleanup
pca.deinit()