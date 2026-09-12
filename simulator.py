from meter import Meter
import time

class Simulator:
    def __init__(self, number_of_meters):

        self.meters=[]

        for number in range(1, number_of_meters +1):
            meter_id=f"MTR-{number:05d}"
            meter=Meter(meter_id)
            self.meters.append(meter)

    def generate_readings(self):
        readings=[]

        for meter in self.meters:
            reading=meter.generate_reading()
            readings.append(reading)

        return readings

    def run(self, interval):
        while True:
            readings=self.generate_readings()
            for reading in readings:
                print(
                    f"{reading.meter_id} |"
                    f"Flow: {reading.flow_rate} L/S |"
                    f"Consumption: {reading.total_consumption} L"
                    f"timestamp: {reading.timestamp.isoformat()}"      
                )

            time.sleep(5)
            


    def set_meter_mode(self, meter_id, mode):
        for meter in self.meters:
            if meter.meter_id==meter_id:
                meter.mode=mode
                return

        print(f"Meter {meter_id} not found!")

