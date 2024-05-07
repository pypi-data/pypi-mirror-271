import datetime


class Measure:
    def __init__(self, sensor_id: int, measured_at: datetime, temperature: float, humidity: float):
        self.sensor_id = sensor_id
        self.measured_at = measured_at
        self.temperature = temperature
        self.humidity = humidity

    def toJson(self):
        measured_at_formatted = self.measured_at.strftime('%Y-%m-%d %H:%M:%S.%f')
        return {'sensor': self.sensor_id, 'measured_at': measured_at_formatted, 'temperature': self.temperature,
                'humidity': self.humidity}
