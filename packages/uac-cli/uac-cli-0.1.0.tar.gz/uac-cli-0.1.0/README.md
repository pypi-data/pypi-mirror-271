# UAC-CLI: CLI for managing Stonebranch - UAC

## Overview

UAC CLI is a command-line interface tool designed to interact with the Universal Controller API. It provides a comprehensive set of commands for managing resources such as audits, agent clusters, agents, bundles, business services, calendars, cluster nodes, credentials, custom days, database connections, email connections, LDAP configurations, metrics, OAuth clients, OMS servers, PeopleSoft connections, promotion targets, properties, reports, SAP connections, scripts, server operations, simulations, system status, task instances, tasks, triggers, universal events, universal templates, user groups, users, variables, virtual resources, webhooks, and workflows.

## Features

- **Environment Configuration**: Automatically loads environment variables from a `.env` file to simplify configuration management.
- **Logging**: Supports various log levels (DEBUG, INFO, WARNING, ERROR, CRITICAL) to aid in debugging and operational monitoring.
- **Output**: Allows users to specify output file paths for writing the output to .json files.
- **Selective Field Return**: Supports JSONPath expressions to select specific fields from JSON responses for output.
- **Input from Files**: Enables specifying input parameters from files, facilitating complex operations that require detailed configurations.
- **Ignore IDs**: Offers an option to ignore sysIDs in payloads, streamlining the creation of new resources without manual ID removal.

## Installation

Before installing UAC CLI, ensure you have Python installed on your system. It's recommended to use Python 3.6 or higher.

```bash
pip install uac-cli
```

## Configuration

Run the init command so that it will create a profile file for you. Default profile name is 'default'
```bash
uac config init    
Please enter UAC URL []: https://atlanta.stonebranchdev.cloud/
Do you use personal access token? [Y/n]: 
Please enter personal access token []: <token>
Config file written. (Path: /Users/user/.uac/profiles.yml)
```

### Adding new profile
Run the config add-profile command and follow the steps

### Using a profile
Use --profile or -p option

```bash
uac -p dev system get
```

## Usage

The UAC CLI tool is invoked using the `uac` command followed by subcommands and options. Here's the basic syntax:

```bash
uac [OPTIONS] COMMAND [ARGS]...
```

### Global Options

- `--log-level, -l`: Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
- `--help`: Show the help message and exit.

### Commands

The UAC CLI tool includes multiple commands corresponding to different resources and operations. Here's a brief overview of some key commands:

- `audit list`: Get a list of audits.
- `agent_cluster create`: Creates a new Agent Cluster.
- `agent get`: Retrieves information on a specific Agent.
- `bundle list`: Retrieves information on all Bundles.
- `calendar create`: Creates a new Calendar.
- `credential update`: Modifies the Credential specified by the sysId.
- `database get`: Retrieves information on a specific Database Connection.
- `email_template create`: Creates an Email Template.
- `ldap update`: Modifies LDAP configuration.
- `metrics get`: Scrapes the Universal Controller metrics as Prometheus text.
- `oauth_client list`: Retrieves information on all OAuth Clients.
- `oms_server delete`: Deletes the specified OMS Server.
- `peoplesoft create`: Creates a PeopleSoft Connection.
- `property list`: Retrieves information on all properties.
- `report run_report`: Runs a report and outputs in the specified format.
- `sap list`: Retrieves information on all SAP Connections.
- `script delete`: Deletes a Script.
- `server_operation roll_log`: Rolls the log for the server.
- `simulation create`: Creates a new Simulation.
- `system get`: Retrieves system status.
- `task_instance list`: Lists all Task Instances.
- `task create`: Creates a new Task.
- `trigger update`: Modifies a Trigger.
- `universal_event publish`: Publishes a Universal Event.
- `user create`: Creates a new User.
- `variable set`: Sets a Variable.
- `virtual_resource list`: Lists all Virtual Resources.
- `webhook enable`: Enables a Webhook.
- `workflow get_vertices`: Retrieves information on all vertices in a Workflow.

### Examples

### Listing Audits and Agent Clusters

```bash
#!/bin/bash

# List all audits and output the result to a JSON file
uac audit list -o result.json

# List all agent clusters and output the result to a JSON file
uac agent-cluster list -o result.json
```

### Working with Agent Clusters

```bash
# List all agent clusters and get the name of the first one
CLUSTER=$(uac agent-cluster list --select "[0].name")

# Get details of the first agent cluster and output to a file
uac agent-cluster get agent_cluster_name="$CLUSTER" -o agent_cluster.json

# Update the agent cluster using the modified JSON file
uac agent-cluster update --input agent_cluster.json

# Create a new agent cluster using the configuration from the file
uac agent-cluster create --input agent_cluster.json retain_sys_ids='false' name="Huseyin Agent Cluster2"

# Delete the newly created agent cluster
uac agent-cluster delete agentclustername="Huseyin Agent Cluster2"

# List advanced details of the first agent cluster
uac agent-cluster list_advanced agent_cluster_name="${CLUSTER}" -s "$.[0].name"

# Get the selected agent from the first agent cluster
uac agent-cluster get_selected_agent agent_cluster_name="${CLUSTER}" -s "$.queueName"

# Suspend and then resume the first agent cluster
uac agent-cluster suspend agent_cluster_name="${CLUSTER}"
uac agent-cluster resume agent_cluster_name="${CLUSTER}"

# Set the task execution limit for the first agent cluster
uac agent-cluster set_task_execution_limit agent_cluster_name="${CLUSTER}" limit_amount=10 limit_type=limited
uac agent-cluster set_task_execution_limit agent_cluster_name="${CLUSTER}" limit_type=unlimited

# Resolve the network alias for the first agent cluster
uac agent-cluster resolve_cluster agent_cluster_name="${CLUSTER}"
```

### Managing Business Services

```bash
# List all business services and output to a file
uac business-service list -o business_service.json

# Get the last business service's name
BS=$(uac business-service list -s "$.[-1].name")

# Get details of the last business service and output to a file
uac business-service get busservicename=$BS -o bs.json

# Update the business service with a new description
uac business-service update -i bs.json description="updated"

# Create a new business service based on the existing one
uac business-service create -i bs.json name="READONLY2" --ignore-ids

# Delete the newly created business service
uac business-service delete busservicename=READONLY2
```

### Working with Credentials

```bash
# List the last credential's name and set it to a variable
CRED=$(uac credential list -s "$.[-1].name")

# Get details of the last credential and output to a file
uac credential get credentialname="$CRED" -o cred.json

# Update the credential with a new description
uac credential update -i cred.json description="Updated"

# Create a new credential based on the existing one
uac credential create -i cred.json name="dummy2" --ignore-ids

# Delete the newly created credential
uac credential delete credentialid=875b52ee17344a27996c85738b4be14a

# Change the runtime password of the credential
uac credential change_password name=$CRED new_runtime_password=dummy

# Test the provider for the credential
uac -l DEBUG credential test_provider credentialname=dummy
```

### Generating and Managing Metrics

```bash
# Get metrics and output to a JSON file
uac metrics get -o result.json

# Get metrics and filter for a specific metric
uac metrics get | grep -i process_virtual_memory_bytes
```

### Obtaining System Information

```bash
# Get system information and select the memoryFree field
uac system get -s "$.memoryFree"
```

#### Listing All Agents

```bash
uac agent list
```

#### Creating a New Agent Cluster

```bash
uac agent_cluster create --input agent_cluster_config.json --ignore-ids
```

#### Running a Report

```bash
uac report run_report report_title="Active Tasks" --format pdf --output report_output.pdf
```

## Development

To contribute to the UAC CLI tool, clone the repository, make your changes, and submit a pull request. Ensure you follow the project's coding standards and update tests as necessary.

## Support

For issues, questions, or contributions, please submit an issue or pull request on the project's GitHub page.

# Contributing
We welcome contributions! Please refer to our Contributing Guide for details on how to submit pull requests, propose bug fixes and improvements, and how to build and test your changes to this project.

# License

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International License (CC BY-NC 4.0).

### What this means

The CC BY-NC 4.0 License allows others to remix, adapt, and build upon the work non-commercially, as long as they credit the creator and license their new creations under the identical terms.

### Full Legal Code

You can read the full legal code of the license [here](https://creativecommons.org/licenses/by-nc/4.0/legalcode).

### Summary of the License

This summary is a quick guide to the key elements of the full license, which is legally binding:

- **Attribution:** You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

- **NonCommercial:** You may not use the material for commercial purposes.

- **ShareAlike:** If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

- **No additional restrictions:** You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

For more information about what you can and can't do under this license, please review the license code and summary at the provided link.

# Disclaimer
This package is not officially affiliated with Stonebranch, Inc. It is a community-driven project aimed at simplifying the use of Stonebranch UAC APIs.