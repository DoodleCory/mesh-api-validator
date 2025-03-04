import urllib3
import json
import certifi

class RPCClient:
    def __init__(self, base_url, username=None, password=None, verify_ssl=False):
        self.base_url = base_url
        self.username = username
        self.password = password

        # Disable warnings for self-signed certificates
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        # Create a pool manager with SSL verification disabled
        if verify_ssl:
            self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        else:
            self.http = urllib3.PoolManager(cert_reqs='CERT_NONE')

        self.token = None

    def login(self):
        """Authenticates with the radio and gets a token"""
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "call",
            "params": [
                "00000000000000000000000000000000",
                "session",
                "login",
                {"username": self.username, "password": self.password}
            ]
        }

        response = self.http.request(
            'POST',
            self.base_url,
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        data = json.loads(response.data.decode('utf-8'))
        if 'result' in data and len(data['result']) > 1:
            self.token = data['result'][1]['ubus_rpc_session']
            return data

        raise Exception(f"Login failed: {data}")

    def send_request(self, method, params=None, service=None):
        """Send a request using the authenticated token"""
        if self.token is None:
            self.login()

        # Simplify parameter handling for all service calls
        if service:
            full_params = [self.token, service, method, params if params is not None else {}]
        else:
            # Legacy format for non-service calls
            full_params = [self.token] + (method if isinstance(method, list) else [method])
            if params:
                if isinstance(params, list):
                    full_params.extend(params)
                else:
                    full_params.append(params)

        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "call",
            "params": full_params
        }

        # Debug
        #print(f"DEBUG: Sending payload: {json.dumps(payload)}")

        response = self.http.request(
            'POST',
            self.base_url,
            body=json.dumps(payload),
            headers={'Content-Type': 'application/json'}
        )

        return json.loads(response.data.decode('utf-8'))