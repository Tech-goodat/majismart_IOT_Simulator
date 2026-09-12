import random
from datetime import datetime, timezone
from telemetry import Telemetry
class Meter:
    def __init__(self, meter_id):
        self.meter_id=meter_id
        self.flow_rate=0.0
        self.total_consumption=0.0
        self.status="ONLINE"
        self.mode="NORMAL"
        self.last_reading_time=datetime.now(timezone.utc)

    def generate_flow_rate(self):
        if self.mode == "NORMAL":
            return random.uniform(0.0, 3.0)

        if self.mode == "LEAK":
            return random.uniform(4.0, 6.0)

        return 0.0

    def generate_reading(self):
        current_time=datetime.now(timezone.utc)

        elapsed_seconds=( current_time - self.last_reading_time).total_seconds()
        self.flow_rate=self.generate_flow_rate()
        consumption=self.flow_rate * elapsed_seconds
        self.total_consumption += consumption
        self.last_reading_time=current_time

        return Telemetry(
            meter_id=self.meter_id,
            flow_rate=round(self.flow_rate, 2),
            total_consumption=round(self.total_consumption, 2),
            status=self.status,
            timestamp=current_time
        )
