# F5 Distributed Cloud Backup/Restore Operations

[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)
[![GitHub branch checks state](https://img.shields.io/github/checks-status/f5-devcentral/f5xc-backup-restore-utils/main?label=build%20checks)](https://github.com/f5-devcentral/f5xc-backup-restore-utils/actions)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/f5-devcentral/f5xc-backup-restore-utils)](https://github.com/f5-devcentral/f5xc-backup-restore-utils/pulse/monthly)

[![powered by semgrep](https://img.shields.io/badge/powered%20by-semgrep-1B2F3D?labelColor=lightgrey&link=https://semgrep.live/&style=flat-square&logo=data%3Aimage%2Fpng%3Bbase64%2CiVBORw0KGgoAAAANSUhEUgAAAA0AAAAOCAYAAAD0f5bSAAAABmJLR0QA/gD+AP+cH+QUAAAACXBIWXMAAA3XAAAN1wFCKJt4AAAAB3RJTUUH5AYMEy0l8dkqrQAAAvFJREFUKBUB5gIZ/QEAAP8BAAAAAAMG6AD9+hn/GzA//wD//wAAAAD+AAAAAgABAQDl0MEBAwbmAf36GQAAAAAAAQEC9QH//gv/Gi1GFQEC+OoAAAAAAAAAAAABAQAA//8AAAAAAAAAAAD//ggX5tO66gID9AEBFSRxAgYLzRQAAADpAAAAAP7+/gDl0cMPAAAA+wAAAPkbLz39AgICAAAAAAAAAAAs+vU12AEbLz4bAAAA5P8AAAAA//4A5NDDEwEBAO///wABAQEAAP//ABwcMD7hAQEBAAAAAAAAAAAaAgAAAOAAAAAAAQEBAOXRwxUAAADw//8AAgAAAAD//wAAAAAA5OXRwhcAAQEAAAAAAAAAAOICAAAABP3+/gDjzsAT//8A7gAAAAEAAAD+AAAA/wAAAAAAAAAA//8A7ePOwA/+/v4AAAAABAIAAAAAAAAAAAAAAO8AAAABAAAAAAAAAAIAAAABAAAAAAAAAAgAAAD/AAAA8wAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAAA8AAAAEAAAA/gAAAP8AAAADAAAA/gAAAP8AAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAA7wAAAPsAAAARAAAABAAAAP4AAAAAAAAAAgAAABYAAAAAAAAAAAIAAAD8AwICAB0yQP78/v4GAAAA/wAAAPAAAAD9AAAA/wAAAPr9//8aHTJA6AICAgAAAAD8AgAAADIAAAAAAP//AB4wPvgAAAARAQEA/gEBAP4BAQABAAAAGB0vPeIA//8AAAAAAAAAABAC+vUz1QAAAA8AAAAAAwMDABwwPu3//wAe//8AAv//ABAcMD7lAwMDAAAAAAAAAAAG+vU0+QEBAvUB//4L/xotRhUBAvjqAAAAAAAAAAAAAQEAAP//AAAAAAAAAAAA//4IF+bTuuoCA/QBAQAA/wEAAAAAAwboAP36Gf8bMD//AP//AAAAAP4AAAACAAEBAOXQwQEDBuYB/foZAAAAAAD4I6qbK3+1zQAAAABJRU5ErkJggg==)](https://github.com/f5-devcentral/f5xc-backup-restore-utils/actions/workflows/secops-code-scan.yml)

### Introduction

This repository contains tools designed to help network operations staff save and restore the configuration from their F5 Distributed Cloud tenant. These tools are scripts to be run on a Linux server to create a backup file of the configuration settings (backup function) or to apply those settings to a system (restore function).

### Contents

[Prerequisites](#prerequisites)
[Installation](#installation)
[Usage](#usage)
[Example Output](#example-output)

> [!IMPORTANT]
> The following configuration objects are supported for backup and restore functions only:

> - HTTP Load Balancer
> - TCP Load Balancer
> - Origin Servers and Pools
> - Health Check
> - App Firewalls with it WAF exclusion policy
> - API Definition
> - Service Policy
> - Rate Limiter Policy
> - Malicious User Policy
> - User Identification Policy
> - IP Prefix Set
> - Forward Proxy Policy
> - Alert Policy
> - Alert Receiver
> - Global Log Receiver
> - Certificate Management
> - Certificate Management Chain
> - Service Discovery

### Prerequisites

Before using these tools, you need to have the following:

- **Python 3.x**: This is the programming language in which the script is written. You need to have it installed on your system to run the script.
- **F5XC Tenant URL**: This is the web address of your specific network management area.
- **F5XC API Token**: This is a special code that allows the script to access and modify your network settings. You can obtain an API Token by following the instructions provided in the F5 documentation [here](https://docs.cloud.f5.com/docs/how-to/user-mgmt/credentials).
- **Namespace**: Before running the restore function, make sure the namespace (a specific area within your tenant where settings are applied) exists.

### Installation

Refer to [INSTALL.md](/INSTALL.md) for installation instructions.

### Usage

Refer to [USAGE.md](/USAGE.md) for usage instructions.

### Example Output

The following is an example of output from a backup:

```bash

backup-server$python3 f5xc-backup-restore.py -a backup -p /var/backup -n mcn-sample

======================================================================================================================
[STARTED]     Date: 2024-02-21 07:05:26 UTC     Tenant: f5-xctestdrive     TASK: BACKUP       Namespace: mcn-sample
======================================================================================================================
[mcn-sample] Backing up HTTP Loadbalancer object [mcn-sample-lb] ..... DONE
[mcn-sample] Backing up Origin Pool object [mcn-sample-originpool] ..... DONE
[mcn-sample] Backing up Health Check object [mcn-sample-hc] ..... DONE
[mcn-sample] Backing up App Firewall object [mcn-sample-appfw] ..... DONE
[mcn-sample] Backing up Malicious User Mitigation object [mcn-sample-maluser-policy] ..... DONE
================================================================================================================
[COMPLETED]   Date: 2024-02-21 07:05:58 UTC     Tenant: f5-xctestdrive
================================================================================================================

```

The following is an example of output from a restore:

```bash

backup-server$python3 f5xc-backup-restore.py -a restore -p /var/backup/f5xc-backup-20240221_070526/ -n mcn-sample

==================================================================================================================================
[STARTED]     Date: 2024-02-21 07:09:50 UTC      Tenant: f5-xctestdrive    TASK: RESTORE      Namespace: mcn-sample
====================================================================================================================================
[mcn-sample] Restoring Health Check object from file [ mcn-sample_healthcheck-mcn-sample-hc.json ] ..... DONE
[mcn-sample] Restoring Origin Pool object from file [ mcn-sample_origin_pool-mcn-sample-originpool.json ] ..... DONE
[mcn-sample] Restoring App Firewall object from file [ mcn-sample_app_fw-mcn-sample-appfw.json ] ..... DONE
[mcn-sample] Restoring HTTP LoadBalancer object from file [ mcn-sample_http_lb-mcn-sample-lb.json ] ..... DONE
[mcn-sample] Restoring Malicious User Policy object from file [ mcn-sample_malicioususer_policy-mcn-sample-maluser-policy.json ] ..... DONE
================================================================================================================
[COMPLETED]   Date: 2024-02-21 07:10:20 UTC     Tenant: f5-xctestdrive
================================================================================================================
```
