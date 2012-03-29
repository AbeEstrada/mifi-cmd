MiFi-Cmd
========
This is a command line tool to get the status of a MiFi device.

Requirements
------------
* Python 2.7+
* Beautiful Soup 4.x ```pip install beautifulsoup4```

Devices supported
-----------------
* MiFi 2200

How to use
----------
```mifi``` - current status of the MiFi device

```mifi connect``` - to connect to the current network if the status is "Disconnected"

```mifi disconnect``` - to disconnect from the current network if connected (or dormant)
