from sense_hat import SenseHat

class AccelerationDataProvider:
  def __init__(self) -> None:
    self.sense = SenseHat()
    self.sense.set_imu_config(False, False, True)
  
  def get(self):
    return self.sense.get_accelerometer_raw()