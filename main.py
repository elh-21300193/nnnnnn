import json
import requests
import os

# Crear el directorio Data si no existe
if not os.path.exists('./Data'):
    os.makedirs('./Data')

def formar_json():
    dict_data = {
        'switches': [
            {"model1": 'CAT9300', "model2": 'CAT9400'},
            {"model3": 'CAT9500', "model4": 'CAT9600'}
        ],
        'routers': [
            {'name': 'ISR4451-X', 'vendor': 'cisco', 'type': 'hardware'},
            {'name': 'ASR1001-X', 'vendor': 'cisco', 'type': 'hardware'}
        ]
    }

    # Imprimir JSON en formato legible
    print(json.dumps(dict_data, indent=4, sort_keys=True))

    # Guardar el JSON en un archivo
    with open("./Data/dispositivos.json", 'w') as file:
        json.dump(dict_data, file, indent=4, sort_keys=True)

def infraestructura_json():
    network_dict = {
        'servers': [
            {"server1": {'name': 'srv1', 'os': 'ubuntu', 'services': ['nginx', 'ssh']}},
            {"server2": {'name': 'srv2', 'os': 'centos', 'services': ['apache', 'mysql']}},
            {"server3": {'name': 'srv3', 'os': 'debian', 'services': ['ftp', 'dns']}}
        ],
        'databases': [
            {"db1": {'name': 'db1', 'type': 'SQL', 'version': '5.7'}},
            {"db2": {'name': 'db2', 'type': 'NoSQL', 'version': '4.0'}}
        ]
    }

    # Imprimir JSON en formato legible
    print(json.dumps(network_dict, indent=4, sort_keys=True))

    # Guardar el JSON en un archivo
    with open("./Data/infraestructura.json", 'w') as file:
        json.dump(network_dict, file, indent=4, sort_keys=True)


def get_meraki_devices(api_key):
    url = 'https://api.meraki.com/api/v1/organizations/1578878/devices'
    headers = {
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            devices = response.json()
            with open("./Data/meraki_devices.json", 'w') as file:
                json.dump(devices, file, indent=4, sort_keys=True)

            if not devices:
                print("No devices found for this organization.")
            else:
                for device in devices:
                    print(
                        f"Device Name: {device.get('name')}, Model: {device.get('model')}, Serial: {device.get('serial')}")
        else:
            with open("./Data/meraki_devices.json", 'w') as file:
                file.write(
                    f"Failed to get data from Cisco Meraki API, status code: {response.status_code}, response text: {response.text}")
            print(
                f"Failed to get data from Cisco Meraki API, status code: {response.status_code}, response text: {response.text}")
    except requests.exceptions.RequestException as e:
        with open("./Data/meraki_devices.json", 'w') as file:
            file.write(f"Failed to connect to Cisco Meraki API: {str(e)}")
        print(f"Failed to connect to Cisco Meraki API: {str(e)}")


def get_api_ips(api_key):
    urls = [
        'http://ip-api.com/json/8.8.8.8',
        'http://ip-api.com/json/24.48.0.1?fields=message,timezone,isp',
        'http://ip-api.com/json/1.1.1.1?fields=status,country,regionName,lat,as'
    ]

    responses = []
    for url in urls:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            selected_data = {
                'status': data.get('status'),
                'country': data.get('country'),
                'lat': data.get('lat'),
                'lon': data.get('lon'),
                'regionName': data.get('regionName'),
                'isp': data.get('isp'),
                'org': data.get('org'),
                'query': data.get('query')
            }
            responses.append(selected_data)
        else:
            print(f"Failed to get data from {url}")

    # Imprimir respuestas en formato legible
    print(json.dumps(responses, indent=4, sort_keys=True))

    # Guardar respuestas en un archivo JSON
    with open("./Data/api_responses.json", 'w') as file:
        json.dump(responses, file, indent=4, sort_keys=True)

def get_meraki_organizations(api_key):
    url = 'https://api.meraki.com/api/v1/organizations'
    headers = {
        'Content-Type': 'application/json',
        'X-Cisco-Meraki-API-Key': api_key
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        organizations = response.json()
        with open("./Data/meraki_organizations.json", 'w') as file:
            json.dump(organizations, file, indent=4, sort_keys=True)
        for org in organizations:
            print(f"ID: {org['id']}, Name: {org['name']}")
    else:
        print(
            f"Failed to get data from Cisco Meraki API, status code: {response.status_code}, response text: {response.text}")




if __name__ == '__main__':
    formar_json()
    infraestructura_json()
    api_key = '8dd5430fcdaaa6f70a0f861bc88adeffcca4c87e'
    get_meraki_devices(api_key)
    get_api_ips(api_key)
    get_meraki_organizations(api_key)
