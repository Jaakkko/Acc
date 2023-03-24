import time
import numpy

class TestDataProvider:
  def get(self):
    time.sleep(0.01)
    return {
      "x": 10 * numpy.sin(0.2 * 2 * numpy.pi * time.time_ns() / 1_000_000_000)
    }