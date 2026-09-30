from dataclasses import dataclass
from datetime import datetime


@dataclass
class Telemetry:
    meter_id: str
    flow_rate: float
    total_consumption: float
    status: str
    valve_open: bool
    closure_source: str
    timestamp: datetime

    def to_dict(self):
        return {
            "meter_id": self.meter_id,
            "flow_rate": self.flow_rate,
            "total_consumption": self.total_consumption,
            "status": self.status,
            "valve_open": self.valve_open,
            "closure_source": self.closure_source,
            "timestamp": self.timestamp.isoformat()
        }