# tests/test_network_settings.py

import unittest
import json
from tests.connectivity_test import BaseTest
from core.test_manager import TestManager
from core.test_mixin import TestMixin
class TestNetworkConnection(BaseTest, TestMixin):
    """Tests the network connection functionality."""
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.test_manager = TestManager(cls.config)

    def test_get_ip(self):
        """Test retrieving the device IP"""
        self.run_test_command("GetIP")

    def test_get_ip_uci_call(self):
        """Test retrieving the device IP using UCI"""
        self.run_test_command("GetIPUCICall")

    def test_get_tx_power(self):
        """Test retrieving the device TX power"""
        self.run_test_command("GetPower")


if __name__ == "__main__":
    unittest.main()