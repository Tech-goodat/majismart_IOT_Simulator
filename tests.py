from simulator import Simulator

simulator=Simulator(5)
simulator.set_meter_mode("MTR-00002", "LEAK")
readings=simulator.generate_readings()

for reading in readings:
    print(
        f"{reading.meter_id} | "
        f"Flow: {reading.flow_rate} L/s | "
        f"Consumption: {reading.total_consumption} L"

    )