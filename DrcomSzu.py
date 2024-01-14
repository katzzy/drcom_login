import os
import sys
import time
import yaml
import re
import requests


class DrcomSzu(object):
    def __init__(self):
        self.__set_working_directory()
        self.config = self.__get_config()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko)"
                          " Chrome/120.0.0.0 Safari/537.36"
        }
        self.__internet_connectivity = False
        self.check_url = None
        self.login_url = None

    @staticmethod
    def __set_working_directory():
        current_path = os.path.abspath(
            os.path.dirname(
                os.path.realpath(sys.argv[0])))
        current_path = current_path.replace("\\", "/")
        # print("当前工作目录：" + current_path)
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

    def get_public_ip(self):
        r = requests.get("https://ip.cn/api/index?ip=&type=0",
                         headers=self.headers).text
        print("公网IP地址：" + re.findall(r"\"ip\":\"(.*?)\"", r)[0])
        print("公网IP地址所在地：" + re.findall(r"\"address\":\"(.*?)\"", r)[0])

    def __check_internet_connection(self):
        r = requests.get(self.check_url, headers=self.headers).text
        self.__internet_connectivity = (
            True if re.findall(r"<title>(.*?)</title>", r)[0] == "注销页"
            else False
        )

    def get_ip(self):
        r = requests.get(self.check_url, headers=self.headers).text
        self.__check_internet_connection()
        if self.__internet_connectivity:
            ip = re.findall(r"v4ip='(.*?)'", r)[0]
            print("校内IP地址：" + ip)
            return ip
        else:
            ip = re.findall(r"v46ip='(.*?)'", r)[0]
            print("校内IP地址：" + ip)
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

    def login_function(self):
        raise NotImplementedError


class DrcomSzuDormitory(DrcomSzu):
    def __init__(self):
        super().__init__()
        self.check_url = "http://172.30.255.42"
        self.login_url = "http://172.30.255.42:801/eportal/portal/login"

    def login_function(self):
        payload = {
            "callback": "dr1003",
            "login_method": "1",
            "user_account": ",0," + self.config["username"],
            "user_password": self.config["password"],
            "wlan_user_ip": self.get_ip(),
            "wlan_user_ipv6": "",
            "wlan_user_mac": "000000000000",
            "wlan_ac_ip": "",
            "wlan_ac_name": "",
            "jsVersion": "4.1.3",
            "terminal_type": "1",
            "lang": "en",
            "v": "3246",
            "lang": "en"
        }
        drcom_res = requests.get(
            self.login_url,
            params=payload,
            headers=self.headers
        )
        result = re.findall(r"\"result\":(\d)", drcom_res.text)[0]
        if result == "1":
            print("登录成功！")
        elif result == "0":
            print("密码错误！")


class DrcomSzuOffice(DrcomSzu):
    def __init__(self):
        super().__init__()
        self.check_url = "https://drcom.szu.edu.cn/a70.htm"
        self.login_url = "https://drcom.szu.edu.cn/a70.htm"

    def login_function(self):
        drcom_form = {
            "DDDDD": self.config["username"],
            "upass": self.config["password"],
            "0MKKey": "%B5%C7%A1%A1%C2%BC",
        }
        drcom_res = requests.post(
            self.login_url,
            data=drcom_form,
            headers=self.headers
        )
        print("响应内容:%s" % drcom_res.text)
        print("请求头:%s" % drcom_res.request.headers)
        print("登录成功！" if drcom_res.status_code == 200 else "登录失败！")


def drcom_login(drcom_szu, auto_login=False):
    if auto_login:
        drcom_szu.login_auto()
    else:
        drcom_szu.login()


def drcom_user_interface():
    while True:
        print("----------------------------------------")
        print("<<< DrcomSzu >>>")
        print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("----------------------------------------")
        type = input(
            "功能列表：\n"
            "0. 设置账号密码\n"
            "1. 宿舍网络(单次登录)\n"
            "2. 教学区网络(单次登录)\n"
            "3. 宿舍网络(自动续期)\n"
            "4. 教学区网络(自动续期)\n"
            "5. 查询校内ip(仅宿舍网络)\n"
            "6. 查询公网ip\n"
            "100. 退出程序\n"
            "请输入功能编号："
        )
        print("----------------------------------------")
        if type == "0":
            DrcomSzu.set_config()
        elif type == "1":
            drcom_login(DrcomSzuDormitory(), False)
        elif type == "2":
            drcom_login(DrcomSzuOffice(), False)
        elif type == "3":
            drcom_login(DrcomSzuDormitory(), True)
        elif type == "4":
            drcom_login(DrcomSzuOffice(), True)
        elif type == "5":
            DrcomSzuDormitory().get_ip()
        elif type == "6":
            DrcomSzu().get_public_ip()
        elif type == "100":
            break
        else:
            print("输入错误！请重新输入！")
        print("----------------------------------------")
        print("回车键继续...")
        input()
        os.system("cls")


def main():
    drcom_user_interface()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("按下了Ctrl+C!")
    except requests.exceptions.ConnectionError:
        print("网络连接错误！")
        print("可能的原因如下：")
        print("1. 未连接到校园网")
        print("2. 校园网服务器故障")
        print("3. 在宿舍区尝试登录教学区网络")
    except Exception as e:
        print("程序出现错误！")
        print("错误信息：", e)
    finally:
        print("程序已关闭！请按回车键退出...")
        input()
        exit(0)
