from dataclasses import dataclass
from datetime import datetime

@dataclass
class Telemetry:
    meter_id:str
    flow_rate:float
    total_consumption:float
    status:str
    timestamp:datetime