# NETPLY

This script was made to automate network configuration via Netplan on Ubuntu and derivative distributions.

## Table of Contents
- [INSTALLATION](#installation)
- [USAGE](#usage)
  - [DHCP config](#dhcp-config)
  - [Static configuration](#static-configuration)
    - [Configure gateway](#configure-gateway)
    - [Configure DNS](#configure-dns)
- [Modifying the script](#modifying-the-script)

---

## INSTALLATION

Clone the repository:
```bash
git clone https://github.com/rpaniaguaa/netply.git
cd netply
```

Create a virtual environment in the repository:
```bash
python -m venv env
```

Activate the environment:
```bash
source ./env/bin/activate
```

Install the requirements using the **requirements.txt** file:
```bash
pip install -r requirements.txt
```

Build the standalone executable using PyInstaller:
```bash
pyinstaller --clean --onefile main.py
```

Copy the compiled **dist/main** binary to the **/usr/local/bin** path:
```bash
sudo cp dist/main /usr/local/bin/netply
```

Give it execution permissions:
```bash
sudo chmod +x /usr/local/bin/netply
```

Now you can deactivate the virtual environment and clean up the build files (optional):
```bash
deactivate
rm -rf build/ dist/ main.spec
```

## USAGE

Now you can run the program from anywhere in your system by simply typing:
```bash
netply
```

### DHCP config

Enable dhcp config (defaults to dhcp if no configuration type is specified)
```bash
sudo netply enp0s8 dhcp
sudo netply enp0s8
```

### Static configuration

Enable static configuration
```bash
netply enp0s8 static -a 192.168.1.1/24
```

#### Configure gateway

defaults to "default" if no destination specified
```bash
netply enp0s8 static -a 192.168.1.10/24 -v 192.168.1.1
```

#### Configure DNS
```bash
netply enp0s8 static -d 8.8.8.8 [1.1.1.1 [...]]
```

## Modifying the script

If you have changed something in the source code, make sure your virtual environment is active and execute these commands to update the global system command:
```bash
source ./env/bin/activate
```

Remove the old executable:
```bash
sudo rm /usr/local/bin/netply
```

Remove the previous build folders:
```bash
rm -rf build/ dist/ main.spec
```

Recompile **main.py** and clean the PyInstaller cache:
```bash
pyinstaller --clean --onefile main.py
```

Move the new binary back to the system path and give it permissions:
```bash
sudo cp dist/main /usr/local/bin/netply
sudo chmod +x /usr/local/bin/netply
```
