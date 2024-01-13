import os
import sys
import time
import yaml
import requests


class DrcomSzu(object):
    def __init__(self):
        self.__set_working_directory()
        self.config = self.__get_config()
        self.__internet_connectivity = False

    @staticmethod
    def __set_working_directory():
        current_path = os.path.abspath(
            os.path.dirname(
                os.path.realpath(sys.argv[0])))
        current_path = current_path.replace("\\", "/")
        print("当前工作目录：" + current_path)
        os.chdir(current_path)

    def __get_config(self):
        if not os.path.exists("config.yml"):
            print("配置文件不存在！")
            print("正在创建配置文件...")
            self.set_config()
        with open("config.yml", "r") as ymlfile:
            config = yaml.safe_load(ymlfile)
        return config

    @staticmethod
    def set_config():
        print("请输入校园网账号：")
        username = input()
        print("请输入校园网密码：")
        password = input()
        with open("config.yml", "w") as ymlfile:
            cfg = {"username": username, "password": password}
            yaml.dump(cfg, ymlfile)
        print("配置文件更新成功！")

    def __check_internet_connection(self):
        r = requests.get(self.get_url("check")).text
        index = r.find("<title>")
        if r[index + 7: index + 10] == "注销页":
            self.__internet_connectivity = True
        else:
            self.__internet_connectivity = False

    def get_ip(self):
        r = requests.get(self.get_url("check")).text
        self.__check_internet_connection()
        if self.__internet_connectivity:
            index = r.find("v4ip=")
            ip = r[index + 6: index + 18]
            return ip
        else:
            index = r.find("v46ip=")
            ip = r[index + 7: index + 19]
            return ip

    def login(self):
        self.__check_internet_connection()
        if self.__internet_connectivity:
            print("网络已连接！",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        else:
            print("网络未连接！",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("尝试登录...",
                  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            self.login_function()

    def login_auto(self):
        print("注意:请不要设置过短的间隔时间，至少大于5分钟!!!")
        sleep_time = input("请输入自动检测间隔时间(单位：分钟):")
        print("程序将每隔" + sleep_time + "分钟自动检测网络连接状态并登录!")
        print("按下Ctrl+C可退出程序!")
        while True:
            self.login()
            time.sleep(60 * int(sleep_time))

    def get_url(self, type):
        raise NotImplementedError

    def login_function(self):
        raise NotImplementedError


class DrcomSzuDormitory(DrcomSzu):
    def __init__(self):
        super().__init__()

    def get_url(self, type):
        if type == "check":
            return "http://172.30.255.42"
        elif type == "login":
            ip = self.get_ip()
            username = self.config["username"]
            password = self.config["password"]
            print("Local IP: " + ip)
            return (
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

    def login_function(self):
        drcom_res = requests.get(self.get_url("login"))
        print("Response Text: " + drcom_res.text)
        if drcom_res.text[17] == "1":
            print("登录成功！")
        else:
            print("登录失败！")


class DrcomSzuOffice(DrcomSzu):
    def __init__(self):
        super().__init__()

    def get_url(self, type):
        if type == "check":
            return "https://drcom.szu.edu.cn/a70.htm"
        elif type == "login":
            return "https://drcom.szu.edu.cn/a70.htm"

    def login_function(self):
        drcom_form = {
            "DDDDD": self.config["username"],
            "upass": self.config["password"],
            "0MKKey": "%B5%C7%A1%A1%C2%BC",
        }
        drcom_res = requests.post(self.get_url("login"), drcom_form)
        print("Response Text: " + drcom_res.text)
        print("登录成功！" if drcom_res.status_code == 200 else "登录失败！")


def main():
    print("欢迎使用DrcomSzu！")
    type = input(
        "请选择网络类型：\n"
        "0. 设置账号密码\n"
        "1. 宿舍网络(单次登录)\n"
        "2. 教学区网络(单次登录)\n"
        "3. 宿舍网络(自动续期)\n"
        "4. 教学区网络(自动续期)\n"
    )
    match type:
        case "0":
            DrcomSzu.set_config()
        case "1":
            drcom_szu_dormitory = DrcomSzuDormitory()
            drcom_szu_dormitory.login()
        case "2":
            drcom_szu_office = DrcomSzuOffice()
            drcom_szu_office.login()
        case "3":
            drcom_szu_dormitory = DrcomSzuDormitory()
            drcom_szu_dormitory.login_auto()
        case "4":
            drcom_szu_office = DrcomSzuOffice()
            drcom_szu_office.login_auto()
        case _:
            raise ValueError("Invalid type")


if __name__ == "__main__":
    try:
        main()
    except ValueError:
        print("无效的类型！")
    except KeyboardInterrupt:
        print("按下了Ctrl+C!")
    except requests.exceptions.ConnectionError:
        print("网络连接错误！")
        print("可能的原因如下：")
        print("1. 未连接到校园网")
        print("2. 校园网服务器故障")
        print("3. 在宿舍区尝试登录教学区网络")
    finally:
        print("程序执行完成！请按下回车键退出...")
        input()
        exit(0)
