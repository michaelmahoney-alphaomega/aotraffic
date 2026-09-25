from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
import paho.mqtt.client as mqtt_client
from typing import Any

@dataclass
class Sensor_Data(ABC):
    sensor_id: int
    timestamp: datetime
    count_type: Count_Type 

class Sensor:
    def __init__(self, sensor_id: int) -> None:
        self.sensor_id = sensor_id
        self.driver = None
        self.timestamp: datetime
        self.value: int = 1

    def _call_driver(self) -> Any:
        return None
    
    def read_state(self) -> Sensor_Data:
        raw_state = self._call_driver()
        return None

class Count_Type(Enum):
    PEDESTRIAN = 1
    BIKE = 2
    CAR = 3
    TRUCK = 4
    OTHER = 5


class Sensor_Interface:
    def __init__(self, sensor: Sensor, broker_address: str, port: int, topic: str, client_id: str) -> None:
        self.sensor = sensor
        self.mqtt_client = mqtt_client(broker_address, port, topic, client_id)

    def read_sensor_state(self, sensor) -> Sensor_Data:
        sensor.read_state()

    def publish(self, sensor_info: Sensor_Data):
        self.mqtt_client.publish(sensor_info)
        