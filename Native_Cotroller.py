from gpiozero import MCP3008, BME280, OutputDevice
import time
import hx711
import requests  

temperature_sensor = BME280()
co2_sensor = MCP3008(channel=0)
pressure_sensor = BME280()

hx = hx711.HX711(dout_pin=23, pd_sck_pin=24)
hx.set_reading_format("MSB", "MSB")
hx.set_reference_unit(1)

fan = OutputDevice(17)
heater = OutputDevice(18)

temperature_threshold = 25
co2_threshold = 500
weight_threshold = 1000

while True:
    try:
        temperature = temperature_sensor.temperature
        co2_level = co2_sensor.value * 100
        pressure = pressure_sensor.pressure
        weight = hx.get_weight()

        print(f'Temperature: {temperature}°C, CO2 Level: {co2_level} ppm, Weight: {weight} grams')

        if temperature > temperature_threshold:
            fan.on()
        else:
            fan.off()

        if co2_level > co2_threshold:
            heater.on()
        else:
            heater.off()
        if weight > weight_threshold:
            api_url = 'localhost/add_stock'
            payload = {
                'message': 'Weight Increase Alert! Your custom message here.',
                'temperature': temperature,
                'co2_level': co2_level,
                'weight': weight
            }
            headers = {'Content-Type': 'application/json'}

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                print(f'API Response: {response.status_code} - {response.text}')

            except requests.RequestException as e:
                print(f'Error making API request: {e}')
        if time.time() % 604800 == 0:
            api_url_periodic = 'http://localhost/periodic_update'
            payload_periodic = {
                'message': 'Periodic Update',
                'temperature': temperature,
                'co2_level': co2_level,
                'weight': weight
            }
            try:
                response_periodic = requests.post(api_url_periodic, json=payload_periodic, headers=headers)
                print(f'Periodic Update - API Response: {response_periodic.status_code} - {response_periodic.text}')

            except requests.RequestException as e:
                print(f'Error making periodic update API request: {e}')

        time.sleep(5)

    except KeyboardInterrupt:
        fan.off()
        heater.off()
        hx.power_down()

        api_url = 'http://localhost/alert'
        payload = {
            'message': 'Alert! some error in auto mode.',
            'temperature': temperature,
            'co2_level': co2_level,
            'weight': weight
        }
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(api_url, json=payload, headers=headers)
            print(f'API Response: {response.status_code} - {response.text}')

        except requests.RequestException as e:
            print(f'Error making API request: {e}')

        break
