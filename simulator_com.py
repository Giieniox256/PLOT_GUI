import serial
import threading
import time

class SerialSimulator:
    def __init__(self, port_name='COM10', baud_rate=9600):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_port = None
        self.is_running = False

    def start_simulation(self):
        try:
            # Open the virtual serial port
            self.serial_port = serial.Serial(port=self.port_name, baudrate=self.baud_rate, timeout=1)
            self.is_running = True

            # Start a thread to simulate communication
            threading.Thread(target=self.simulate_communication).start()

            print(f"Serial simulation started on {self.port_name} at {self.baud_rate} baud.")

        except Exception as e:
            print(f"Error starting serial simulation: {e}")

    def stop_simulation(self):
        if self.serial_port:
            self.is_running = False
            self.serial_port.close()
            print("Serial simulation stopped.")

    def simulate_communication(self):
        while self.is_running:
            try:
                # Simulate receiving data
                received_data = self.serial_port.read(10)
                if received_data:
                    print(f"Received data: {received_data}")

                # Simulate some processing or actions here
                # ...

                # Simulate sending data
                self.serial_port.write(b"SimulatedData")

                time.sleep(1)  # Simulate a delay

            except Exception as e:
                print(f"Error in simulation: {e}")

if __name__ == "__main__":
    simulator = SerialSimulator()

    try:
        simulator.start_simulation()

        # Keep the main thread alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        simulator.stop_simulation()
