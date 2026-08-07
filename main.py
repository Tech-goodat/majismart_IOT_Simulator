import time

from meter import Meter


meter = Meter("MTR-00001")

for _ in range(5):
    reading = meter.generate_reading()

    print(
        f"{reading.meter_id} | "
        f"Flow: {reading.flow_rate} L/s | "
        f"Consumption: {reading.total_consumption} L"
    )

    time.sleep(2)

meter.mode = "LEAK"

print("\n--- LEAK STARTED ---\n")

for _ in range(5):
    reading = meter.generate_reading()

    print(
        f"{reading.meter_id} | "
        f"Flow: {reading.flow_rate} L/s | "
        f"Consumption: {reading.total_consumption} L"
    )

    time.sleep(2)