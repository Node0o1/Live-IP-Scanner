# Live-IP-Scanner
#### *Type: Terminal Application*
## **Description:**
>Test mass connectivity of LAN devices and/or domain list for internal or external domains using the ICMP protocol. Can be used to help map existing networks and identify rogue devices.
>
>To test a systems domain for connectivity with the ICMP protocol, provide a file of all the sub domains in the given environment. addresses must be seperated by a newline character and ports should be appended to the end of each address using the `:` colon.
>
>example:
>127.0.0.1:1234
>
>Auto detection of the host local ipv4 and subnet mask reguardless of virtual network adapters. Populates a range of local ip addresses appropriate to Class C networks to scan for live devices using ping ICMP protocol on the LAN within the range of the host subnet.
>The results of all responding IP's of currently live devices will be printed to the terminal after which you are promted to whether or not you want to save the results to a file.
>This file can then be used to resolve host names for currently live devices within the LAN subnet which is being scanned (results very depending on security protections and permissions).
>
>Ethernet connection to the host returns all live responses. WIFI may be used but results may be partial.

### A few things to note:
- Still needs support for Linux local device name resolution.
- Currently supports Class C networks. Working to incorporate CIDR notations and subnet ip ranges.
- Python 3.11+ is required to run.
- Pip must be installed and Python should be added to Path.

## **Instructions:**
#### **Download**
- Using CLI, navigate to the folder you wish to download the application and run:
  ```console
  git clone https://github.com/Node0o1/Live-IP-Scanner.git
  ```

#### **setup**
- after downloading, use the CLI to navigate to the directory containing the requirements.txt file and run the following command:
  
  ```console
  python -m pip install requirements.txt
  ```
  or
  
  ```console
  python3 -m pip install requirements.txt
  ```
  depending on your environment.

#### **Run**
  - From within the Live-IP-Scanner directory using CLI:
    ```console
    python main.py
    ```
