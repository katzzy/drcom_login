import os
import sys
import time
import yaml
import requests


def get_config():
    current_path = os.path.abspath(
        os.path.dirname(
            os.path.realpath(sys.argv[0])
        )
    )
    current_path = current_path.replace("\\", "/")
    print("当前工作目录：" + current_path)
    os.chdir(current_path)
    if not os.path.exists("config.yml"):
        print("配置文件不存在！")
        print("正在创建配置文件...")
        print("请输入校园网账号：")
        username = input()
        print("请输入校园网密码：")
        password = input()
        with open("config.yml", "w") as ymlfile:
            cfg = {
                "username": username,
                "password": password
            }
            yaml.dump(cfg, ymlfile)
        print("配置文件创建成功！")
    with open("config.yml", "r") as ymlfile:
        config = yaml.safe_load(ymlfile)
    return config


def check_internet_connection():
    try:
        response = requests.get("http://www.github.com", timeout=1)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def get_ip_dormitory():
    r = requests.get('http://172.30.255.42').text
    index = r.find("v46ip=")
    ip = r[index+7:index+19]
    return ip


def drcom_login_dormitory(username, password):
    ip = get_ip_dormitory()
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


def drcom_login_office(username, password):
    drcom_url = "https://drcom.szu.edu.cn/a70.htm"
    drcom_form = {
        "DDDDD": username,
        "upass": password,
        "0MKKey": "%B5%C7%A1%A1%C2%BC"
        }
    drcom_res = requests.post(drcom_url, drcom_form)
    print("登录成功！"
          if drcom_res.status_code == 200 else "登录失败！")


def drcom_login(config, drcom_login_function):
    if check_internet_connection():
        print("网络已连接！", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    else:
        print("网络未连接！", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("尝试登录...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        username = config['username']
        password = config['password']
        drcom_login_function(username, password)


def main():
    config = get_config()
    type = input("请选择网络类型：\n1. 宿舍网络\n2. 教学区网络\n3. 教学区网络自动续连\n:")
    if type == "1":
        drcom_login(config, drcom_login_dormitory)
    elif type == "2":
        drcom_login(config, drcom_login_office)
    elif type == "3":
        sleep_time = input("请输入自动检测间隔时间（单位：分钟）：")
        print("程序将每隔" + sleep_time + "分钟自动检测网络连接状态并登录！")
        while True:
            drcom_login(config, drcom_login_office)
            time.sleep(60 * int(sleep_time))
    else:
        print("输入错误！")
        print("程序执行完成！请按下回车键退出...")
        input()
        exit(0)


if __name__ == "__main__":
    main()
    print("程序执行完成！请按下回车键退出...")
    input()
    exit(0)
