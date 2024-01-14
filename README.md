# DrcomSzu

DrcomSzu is a tool designed for logging into the SZU campus network.

## Dependencies

- Python 3.10+
- Requests
- PyYAML

## Packaging

To package the Python code into an executable file, use the following command:

```bash
pyinstaller -F -i DrcomSzu.ico DrcomSzu.py
```

## Usage

There are two methods to use this script:

### Method 1

- Download the `DrcomSzu.py` to your local machine.

- Install the required dependencies using one of the following commands:

    ```bash
    conda install requests pyyaml
    ```

    or

    ```bash
    pip install requests pyyaml
    ```

- Run the script with Python.

    ```bash
    python DrcomSzu.py
    ```

### Method 2

- Navigate to the [releases page](https://github.com/katzzy/drcom_login/releases) of this repository.

- Download the latest binary file.

- Execute the downloaded binary file.

## For Linux Users

If you are a Linux user, you can log into the SZU campus network using the curl or wget command as follows.

Replace {yourlocalip}, {youraccount}, and {yourpassword} with your own local IP, username, and password respectively.

### Office Area

```bash
 curl 'https://drcom.szu.edu.cn/a70.htm' -d "DDDDD={youraccount}&upass={yourpassword}&0MKKey=%B5%C7%A1%A1%C2%BC" > /dev/null
```

or

```bash
wget -O /dev/null --post-data "DDDDD={youraccount}&upass={yourpassword}&0MKKey=%B5%C7%A1%A1%C2%BC" https://drcom.szu.edu.cn/a70.htm
```

### Dormitory Area

```bash
curl http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{youraccount}&user_password={yourpassword}&wlan_user_ip={yourlocalip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=en&v=4742&lang=en > /dev/null
```

or

```bash
wget -O /dev/null http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{youraccount}&user_password={yourpassword}&wlan_user_ip={yourlocalip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=en&v=4742&lang=en
```
