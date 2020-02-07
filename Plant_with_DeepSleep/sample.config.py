import machine
import ubinascii

# Global settings

# Network settings
WIFI_SSID = 'SSID'
WIFI_PASSWORD = 'PASSWORD'

# MQTT settings
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())
MQTT_SERVER = "MQTT_SERVER_IP"
MQTT_PORT = MQTT_SERVER_PORT
MQTT_USER = b"MQTT_USER"
MQTT_PASSWORD = b"MQTT_PASSWORD"