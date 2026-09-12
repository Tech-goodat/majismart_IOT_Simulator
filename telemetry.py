from dataclasses import dataclass
from datetime import datetime

@dataclass
class Telemetry:
    meter_id:str
    flow_rate:float
    total_consumption:float
    status:str
    timestamp:datetime

    def to_dict(self):
        return{
            "meter_id":self.meter_id,
            "flow_rate":self.flow_rate,
            "total_consumption":self.total_consumption,
            "status":self.status,
            "timestamp":self.timestamp.isoformat()
        }

    