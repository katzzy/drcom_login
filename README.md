# drcom_login

drcom_login is an tool for logging into szu campus networks.

## Package

command to package the python code into an executable (exe):

```bash
Pyinstaller -F -i DrcomSzu.ico DrcomSzu.py
```

## Linux users

If you are using Linux, you can log in using the curl or wget command as follows.

Replace {yourlocalip} {youraccount} and {yourpassword} with your own local_ip username and password.

### office area

```bash
 curl 'https://drcom.szu.edu.cn/a70.htm' -d "DDDDD={youraccount}&upass={yourpassword}&0MKKey=%B5%C7%A1%A1%C2%BC" > /dev/null
```

or

```bash
wget -O /dev/null --post-data "DDDDD={youraccount}&upass={yourpassword}&0MKKey=%B5%C7%A1%A1%C2%BC" https://drcom.szu.edu.cn/a70.htm
```

### dormitory area

```bash
curl http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{youraccount}&user_password={yourpassword}&wlan_user_ip={yourlocalip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=en&v=4742&lang=en > /dev/null
```

or

```bash
wget -O /dev/null http://172.30.255.42:801/eportal/portal/login?callback=dr1003&login_method=1&user_account=%2C0%2C{youraccount}&user_password={yourpassword}&wlan_user_ip={yourlocalip}&wlan_user_ipv6=&wlan_user_mac=000000000000&wlan_ac_ip=&wlan_ac_name=&jsVersion=4.1.3&terminal_type=1&lang=en&v=4742&lang=en
```
