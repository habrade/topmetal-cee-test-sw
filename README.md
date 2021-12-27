
# TopMetal-CEE Testing Software
This is the software for testing TopMetal-CEE Asic. 
The Software is development base on IPbus-Software(https://github.com/ipbus/ipbus-software.git).
So you must install IPbus-Software firstly.

Note: When you install IPbus-Software, be sure to build **Python3 API**.
Example building option:
``` bash
make Set=uhal BUILD_UHAL_PYTHON=1 PYTHON=/usr/bin/python3  -j12
```
Check whether IPbus-Software built properly:
```bash
python3 -c "import uhal"
```
## Setup Environment
1. Install requirement packages
    ```bash
    python3 -m pip install -r requirements.txt 
    ```
2. Running script
    ```bash
   ./run.py
    ```
