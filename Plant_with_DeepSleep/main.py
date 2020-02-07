import time
import ubinascii
import machine
import micropython
import network
import esp
from umqtt.simple import MQTTClient
import config
esp.osdebug(None)
import gc
from ntptime import settime

# Start garbageCollector
gc.collect()
led = machine.Pin(0, machine.Pin.OUT)
mqtt = MQTTClient(
                  config.MQTT_CLIENT_ID,
                  config.MQTT_SERVER,
                  config.MQTT_PORT,
                  config.MQTT_USER,
                  config.MQTT_PASSWORD
                  )

try:
    _adc = machine.ADC(0)
except Exception:
    error.add_error("ADC is not defined")


def do_connect_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)

        sta_if.connect(
                       config.WIFI_SSID,
                       config.WIFI_PASSWORD
                       )
        print('full success')
        while not sta_if.isconnected():
            pass


def get_soil_data():
    adc_max = 1024
    led = machine.Pin(0, machine.Pin.OUT)
    mqtt.connect()
    count_of_results = 10
    init_read = 100 - (_adc.read() * 100) // adc_max
    print('Initial Read is: ', init_read)
    x = 0
    sum = 0
    while x < count_of_results:
        adc_read = _adc.read() * 100
        result = 100 - adc_read // adc_max
        sum += result
        print('Soil: ', result)
        x = x + 1
        time.sleep(1)
    checking_value = sum // count_of_results
    print('Result for this time is: ', checking_value)
    # mqtt.publish('sensors/plant_1'.format(CLIENT_ID).encode(), str(result).encode())


# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# check if the device woke from a deep sleep
if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('woke from a deep sleep')
    led.on();
    do_connect_wifi()  # Connect to WIFI
    get_soil_data()

# set RTC.ALARM0 to fire after 10 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 10000)
# put the device to sleep
print('did all my job. Time to sleep...')
led.off();
machine.deepsleep()
