# mesh_validator/command_definitions/command_builder.py

import yaml
import os

class CommandBuilder:
    """
    Base class for commands.
    Each command type must implement at least 'build_rpc_method' and 'build_rpc_params'.
    """
    def __init__(self, name, **kwargs):
        self.name = name  # e.g., "SetWiFiChannel"
        self.command_definitions = self.load_command_definitions()
        self.params = self.build_rpc_params()
        self.params.update(kwargs)

    def load_command_definitions(self):
        config_path = os.path.join("config", "command_definitions.yaml")
        with open(config_path, "r") as f:
            return yaml.safe_load(f)["commands"]

    def build_rpc_method(self):
        if self.name in self.command_definitions:
            return self.command_definitions[self.name]["method"]
        raise NotImplementedError(f"RPC method for {self.name} not defined")

    def build_rpc_params(self):
        if self.name in self.command_definitions:
            return self.command_definitions[self.name]["params"]
        raise NotImplementedError(f"RPC params for {self.name} not defined")

    def build_rpc_subsystem(self):
        if self.name in self.command_definitions:
            return self.command_definitions[self.name].get("subsystem", None)
        return None

    def execute(self, rpc_client):
        method = self.build_rpc_method()
        subsystem = self.build_rpc_subsystem()
        response = rpc_client.send_request(method, self.params, subsystem)
        #print(f"DEBUG: Response: {response}")
        return response