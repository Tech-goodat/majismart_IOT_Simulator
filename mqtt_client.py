import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker="localhost", port=1883):
        self.broker=broker
        self.port=port
        self.client=mqtt.Client()

    def connect(self):
        self.client.connect(self.broker, self.port)
        self.client.loop_start()
        print("Connected to MQTT broker")

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

