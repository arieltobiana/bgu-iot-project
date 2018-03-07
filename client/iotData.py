from sense_hat import SenseHat
import json
import time

def getInfoConfig():
  sense = SenseHat()
  info = {"date" : time.ctime(),
          "temp" : sense.temp,
          "humidity" : sense.humidity,
          "temperature_from_humidity" : sense.get_temperature_from_humidity(),
          "temperature_from_pressure" : sense.get_temperature_from_pressure(),
          "pressure" : sense.pressure}
  return json.dumps(info)
          