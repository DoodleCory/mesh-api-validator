# rpc/test_manager.py

import json
import os
from .rpc_client import RPCClient
from core.command_builder import CommandBuilder

class TestManager:
    def __init__(self, config, log_dir="logs"):
        self.config = config
        self.log_dir = log_dir
        self.rpc_client = RPCClient(
            base_url=self.config["rpc"]["url"],
            username=self.config["rpc"].get("username"),
            password=self.config["rpc"].get("password")
        )
        self.expected_responses = self.load_expected_responses()

    def load_expected_responses(self):
        data_path = os.path.join(
            os.path.dirname(__file__),
            "..",
            "config",
            "expected_responses.json"
        )
        with open(data_path, "r") as f:
            return json.load(f)

    def run_command(self, command: CommandBuilder):
        method = command.build_rpc_method()
        params = command.build_rpc_params()

        # Send JSON-RPC request
        response = self.rpc_client.send_request(method, params)

        # Log response
        self.log_response(command.name, response)

        # Compare to expected
        is_valid = self.compare_with_expected(command.name, response)
        return is_valid, response

    def compare_responses(self, actual, expected):
        """Compare actual and expected responses, allowing for wildcard values."""
        if isinstance(expected, dict):
            for key, value in expected.items():
                if key not in actual:
                    print(f"DEBUG: Key '{key}' not found in actual response")
                    return False
                if value == "*":  # Allow wildcard values
                    continue
                if not self.compare_responses(actual[key], value):
                    print(f"DEBUG: Value mismatch for key '{key}': expected {value}, got {actual[key]}")
                    return False
        elif isinstance(expected, list):
            if len(actual) != len(expected):
                print(f"DEBUG: List length mismatch: expected {len(expected)}, got {len(actual)}")
                return False
            for act, exp in zip(actual, expected):
                if not self.compare_responses(act, exp):
                    print(f"DEBUG: List item mismatch: expected {exp}, got {act}")
                    return False
        else:
            if expected == "*":  # Allow wildcard values
                return True
            if actual != expected:
                print(f"DEBUG: Value mismatch: expected {expected}, got {actual}")
                return False
        return True

    def compare_with_expected(self, cmd_name, response):
        expected = self.expected_responses.get(cmd_name, None)
        if not expected:
            print(f"DEBUG: No expected response for command '{cmd_name}'")
            return False

        return self.compare_responses(response, expected)

    def log_response(self, cmd_name, response):
        """
        Write JSON response to a log file named after the command or date/time.
        """
        os.makedirs(self.log_dir, exist_ok=True)
        logfile = os.path.join(self.log_dir, f"{cmd_name}.log")
        with open(logfile, "a") as f:
            f.write(json.dumps(response, indent=2))
            f.write("\n")

    def run_all_commands(self, commands):
        results = {}
        for cmd in commands:
            valid, resp = self.run_command(cmd)
            results[cmd.name] = valid
        return results