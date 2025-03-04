# This file contains a mixin class that can be used to test commands in a test case class.
import unittest
from core.command_builder import CommandBuilder
import json

class TestMixin:
    def run_test_command(self, command_name: str):
        cmd = CommandBuilder(command_name)
        response = cmd.execute(self.client)
        #print(f"DEBUG: Response for {command_name}: {json.dumps(response, indent=2)}")
        self.assertIn("result", response)

        # For file service commands, the result structure is different
        cmd_def = cmd.command_definitions.get(command_name, {})
        service = cmd_def.get("service")

        # Skip length validation for file service commands or validate differently
        if service != "file":
            self.assertGreaterEqual(len(response["result"]), 2)

        is_valid = self.test_manager.compare_with_expected(command_name, response)
        self.assertTrue(is_valid, f"Expected response does not match actual response: {response}")
        return response