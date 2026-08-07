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
            print (readings[0])
            time.sleep(interval)