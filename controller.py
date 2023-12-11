import math


# Function to calculate inverse kinematics for a two-segmented arm
def calculate_inverse_kinematics(x, y, L1, L2):
    # Calculate theta2
    theta2 = math.acos((x ** 2 + y ** 2 - L1 ** 2 - L2 ** 2) / (2 * L1 * L2))

    # Calculate theta1
    theta1 = math.atan2(y, x) - math.atan2(L2 * math.sin(theta2), L1 + L2 * math.cos(theta2))

    # Convert angles to degrees
    theta1 = math.degrees(theta1)
    theta2 = math.degrees(theta2)

    return theta1, theta2


# Example arm lengths
L1 = 2.0
L2 = 3.0

# Infinite loop to take user input
while True:
    # Get end-effector position from user
    try:
        x, y = map(float, input("Enter end-effector position (x y): ").split())
    except ValueError:
        print("Invalid input. Please enter numeric values.")
        continue

    # Calculate inverse kinematics
    theta1, theta2 = calculate_inverse_kinematics(x, y, L1, L2)

    # Print the results
    print(f"Theta1: {theta1:.2f} degrees")
    print(f"Theta2: {theta2:.2f} degrees")
