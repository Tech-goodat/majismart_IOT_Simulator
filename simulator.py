import time

from meter import Meter


class Simulator:

    def __init__(self, meters=None):

        self.meters = {}

        if meters is None:
            meters = []

        for meter_data in meters:

            self.add_meter(
                meter_id=meter_data["meter_number"],
                valve_open=meter_data["valve_open"],
                closure_source=meter_data["closure_source"]
            )

    def generate_readings(self):

        readings = []

        for meter in self.meters.values():

            reading = meter.generate_reading()

            readings.append(reading)

        return readings

    def sync_active_meters(
        self,
        active_meters
    ):

        active_meter_ids = {
            meter["meter_number"]
            for meter in active_meters
        }

        current_meter_ids = set(
            self.meters.keys()
        )

        meters_to_add = (
            active_meter_ids
            - current_meter_ids
        )

        meters_to_remove = (
            current_meter_ids
            - active_meter_ids
        )

        for meter_data in active_meters:

            meter_id = meter_data[
                "meter_number"
            ]

            if meter_id in meters_to_add:

                self.add_meter(
                    meter_id=meter_id,
                    valve_open=meter_data[
                        "valve_open"
                    ],
                    closure_source=meter_data[
                        "closure_source"
                    ]
                )

        for meter_id in meters_to_remove:

            self.remove_meter(
                meter_id
            )

    def set_valve_state(
        self,
        meter_id,
        valve_open,
        closure_source
    ):

        meter = self.meters.get(
            meter_id
        )

        if meter is None:

            print(
                f"Cannot update valve. "
                f"Meter {meter_id} is not active."
            )

            return

        meter.valve_open = valve_open

        meter.closure_source = (
            closure_source
        )

        print(
            f"{meter_id} valve "
            f"{'OPENED' if valve_open else 'CLOSED'} "
            f"by {closure_source}"
        )

    def add_meter(
        self,
        meter_id,
        valve_open=True,
        closure_source="NONE"
    ):

        meter_id = meter_id.strip()

        if not meter_id:
            return

        if meter_id in self.meters:

            print(
                f"Meter {meter_id} "
                f"is already active."
            )

            return

        meter = Meter(
            meter_id
        )

        meter.valve_open = valve_open

        meter.closure_source = (
            closure_source
        )

        self.meters[meter_id] = meter

        print(
            f"Started simulation "
            f"for {meter_id} | "
            f"Valve: "
            f"{'OPEN' if valve_open else 'CLOSED'} | "
            f"Closure source: "
            f"{closure_source}"
        )

    def remove_meter(self, meter_id):

        if meter_id not in self.meters:

            print(
                f"Meter {meter_id} "
                f"is not active."
            )

            return

        del self.meters[meter_id]

        print(
            f"Stopped simulation "
            f"for {meter_id}"
        )

    def get_meter(self, meter_id):

        return self.meters.get(
            meter_id
        )

    def run(self, interval):

        while True:

            readings = self.generate_readings()

            for reading in readings:

                print(
                    f"{reading.meter_id} | "
                    f"Flow: "
                    f"{reading.flow_rate} L/S | "
                    f"Consumption: "
                    f"{reading.total_consumption} L | "
                    f"Valve: "
                    f"{'OPEN' if reading.valve_open else 'CLOSED'} | "
                    f"Timestamp: "
                    f"{reading.timestamp.isoformat()}"
                )

            time.sleep(interval)