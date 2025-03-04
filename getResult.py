#!/usr/bin/python3

import requests
import json
import yaml
import os

IPADDR = "10.223.82.95"
USER = "user"
PW = "DoodleSmartRadio"
COMMAND = "GetPower"  # Specify the command to run

url = f'https://{IPADDR}/ubus'

# Disable warnings for self-signed certificates
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Load command definitions from YAML file
def load_command_definitions():
    config_path = os.path.join("config", "command_definitions.yaml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)["commands"]

command_definitions = load_command_definitions()

if COMMAND not in command_definitions:
    raise ValueError(f"Command '{COMMAND}' not found in command definitions")

command_info = command_definitions[COMMAND]

# Create a session
session = requests.Session()

# JSON payload for login request
login_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "call",
    "params": ["00000000000000000000000000000000", "session", "login", {"username": USER, "password": PW}]
}

# Send the login POST request
response = session.post(url, json=login_payload, verify=False)
data = response.json()

# Extract the token
token = data['result'][1]['ubus_rpc_session']

# Build the JSON payload for the specified command
command_payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "call",
    "params": [token, command_info.get("service", ""), command_info["method"], command_info["params"]]
}

# Send the command POST request
response = session.post(url, json=command_payload, verify=False)
data = response.json()


# Print the JSON result
print(json.dumps(data, indent=4, ensure_ascii=False))

# Optional: Also print the stdout content directly
print("\nFormatted stdout content:")
print(data['result'][1]['stdout'])
session.close()