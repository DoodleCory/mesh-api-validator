
<div align="center">
  <img src="https://cdn.builtin.com/cdn-cgi/image/f=auto,fit=cover,w=2580,h=480,q=80/https://builtinla.com/sites/www.builtinla.com/files/2024-10/dheader.png" alt="Doodle Labs Logo" width="250">
  
  <h2>
    ⚠️ 🔥 <span style="color:red"><strong>WORK IN PROGRESS</strong></span> 🔥 ⚠️
  </h2>
  <p><i>This project is under active development and is not yet ready for production use</i></p>
</div>

# Doodle Labs Mesh API Validator

A Python-based testing framework for validating the JSON-RPC API of Doodle Labs' Mesh Rider Radios

## Overview

This tool provides an automated testing environment for Mesh Rider Radios. Functions include:

- Test Suite for validating Mesh Rider API Commands
- Regression Testing for new firmware releases 
- Run configurable tests
- Generate test reports

# Project Structure
    meshrider_api_validator/   
    ├── config/ # Configuration files  
    │ ├── command_definitions.yaml # YAML definitions of RPC commands   
    │ └── expected_responses.json # Expected API responses for testing  
    ├── core/ # Core framework components  
    │ ├── command_builder.py # Builds RPC commands from definitions  
    │ ├── rpc_client.py # JSON-RPC client for API communication  
    │ ├── test_manager.py # Manages test execution and validation  
    │ └── test_mixin.py # mixin class for test commands  
    ├── logs/ # Log output directory  
    ├── tests/ # Test suites
    └── getResult.py # script to discover output of a single command  


## Components

### Core

- **CommandBuilder**: Constructs RPC call based on YAML definitions
- **RPCClient**: Handles authentication and communication with the radio's JSON-RPC API
- **TestManager**: Manages tests, compares responses, and logs results

### Configuration

- **command_definitions.yaml**: Contains definitions for all RPC commands
- **expected_responses.json**: Defines expected responses for validation

### Tests

The `tests/` directory contains test suites that use the framework to validate radio functionality.

### Utilities

- **getResult.py**: A standalone script for running individual commands directly