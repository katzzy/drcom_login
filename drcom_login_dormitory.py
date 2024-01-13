import requests
import yaml
import os
import sys


def get_config():
    current_path = os.path.abspath(
        os.path.dirname(
            os.path.realpath(sys.argv[0])
        )
    )
    current_path = current_path.replace("\\", "/")
    print("当前目录：" + current_path)
    os.chdir(current_path)
    if not os.path.exists("config.yml"):
        print("配置文件不存在！")
        print("正在创建配置文件...")
        with open("config.yml", "w") as ymlfile:
            cfg = {
                "username": "201600000000",
                "password": "123456"
            }
            yaml.dump(cfg, ymlfile)
        print("配置文件创建成功！")
        print("请修改配置文件后重新运行程序！")
        print("程序执行完成！请按下回车键退出...")
        input()
        exit(0)
    with open("config.yml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config


def check_internet_connection():
    try:
        response = requests.get("http://www.github.com", timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def drcom_login(username, password):
    ip = get_ip()
    print("Local IP: " + ip)
    url = (
        "http://172.30.255.42:801/eportal/portal/login?callback=dr1003"
        + "&login_method=1"
        + "&user_account=%2C0%2C" + username
        + "&user_password=" + password
        + "&wlan_user_ip=" + ip
        + "&wlan_user_ipv6="
        + "&wlan_user_mac=000000000000"
        + "&wlan_ac_ip="
        + "&wlan_ac_name="
        + "&jsVersion=4.1.3"
        + "&terminal_type=1"
        + "&lang=en&v=3246&lang=en"
    )

    r = requests.get(url)
    print("Status Code: " + str(r.status_code))
    print("Response Text: " + r.text)
    print(r.text[17])
    if r.text[17] == "1":
        print("登录成功！")
    else:
        print("登录失败！")


def main():
    if check_internet_connection():
        print("网络已连接！")
    else:
        print("网络未连接！")
        print("尝试登录...")
        config = get_config()
        username = config['username']
        password = config['password']
        drcom_login(username, password)


def get_ip():
    r = requests.get('http://172.30.255.42').text
    index = r.find("v46ip=")
    ip = r[index+7:index+19]
    return ip


if __name__ == "__main__":
    main()
    print("程序执行完成！请按下回车键退出...")
    input()
