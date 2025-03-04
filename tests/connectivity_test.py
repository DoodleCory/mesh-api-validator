import unittest
import yaml
import os
from core.rpc_client import RPCClient

class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Load configuration
        config_path = os.path.join("config", "radio_config.yaml")
        with open(config_path, "r") as f:
            cls.config = yaml.safe_load(f)

        # Use the URL directly from config without modification
        base_url = cls.config['rpc']['url']

        # Create RPC client
        cls.client = RPCClient(
            base_url=base_url,
            username=cls.config["rpc"]["username"],
            password=cls.config["rpc"]["password"],
            verify_ssl=False
        )

        # Login once and store the token
        try:
            cls.client.login()
            print(f"Setup complete, logged in with token: {cls.client.token}")
        except Exception as e:
            cls.fail(f"Login failed: {e}")

    @classmethod
    def tearDownClass(cls):
        cls.client = None