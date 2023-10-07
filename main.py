import time
from prometheus_client import start_http_server, Gauge
import routeros_api

MIKROTIK_HOST = '10.0.226.7'
MIKROTIK_USERNAME = 'prometheus'
MIKROTIK_PASSWORD = 'prometheus'
MIKROTIK_PORT = 8728

fan1_speed = Gauge('mikrotik_fan1_speed_rpm', 'Fan1 speed in RPM')
fan2_speed = Gauge('mikrotik_fan2_speed_rpm', 'Fan2 speed in RPM')
fan3_speed = Gauge('mikrotik_fan3_speed_rpm', 'Fan3 speed in RPM')
psu1_state = Gauge('mikrotik_psu1_state', 'Psu1 state 1=ok or 0=fail')
psu2_state = Gauge('mikrotik_psu2_state', 'Psu2 state 1=ok or 0=fail')

def fetch_and_export_system_health():
    connection = routeros_api.RouterOsApiPool(MIKROTIK_HOST,username=MIKROTIK_USERNAME,password=MIKROTIK_PASSWORD,port=MIKROTIK_PORT,plaintext_login=True)
    api = connection.get_api()
    system_health_data = api.get_resource('/system/health').get()
    for item in system_health_data:
        name = item['name']
        value = item['value']
        print(name, value)
        if name == 'fan1-speed':
            fan1_speed.set(float(value))
            print(fan1_speed)
        elif name == 'fan2-speed':
            fan2_speed.set(float(value))
            print(fan2_speed)
        elif name == 'fan3-speed':
            fan3_speed.set(float(value))
            print(fan3_speed)
        elif name == 'psu1-state':
            if value == "ok":
                psu1_state.set(float(1)) ## ok
            else:
                psu1_state.set(float(0)) ## faill
            print(psu1_state)
        elif name == 'psu2-state':
            if value == "ok":
                psu2_state.set(float(1.0)) ## ok
            else:
                psu2_state.set(float(0.0)) ## faill
            print(psu2_state)
    connection.disconnect()
    
if __name__ == "__main__":
    # Start Prometheus HTTP server
    start_http_server(8000)  # Serving metrics on port 8000

    while True:
        fetch_and_export_system_health()
        time.sleep(60)  # Fetch stats every 60 seconds
