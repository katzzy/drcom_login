import os
import sys
import time
import yaml
import re
import requests


class DrcomSzu(object):
    def __init__(self):
        self._config = None
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/120.0.0.0 Safari/537.36"
        }
        self.__internet_connectivity = False
        self.__set_working_directory()
        self.__get_config()

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

    @staticmethod
    def __set_working_directory():
        current_path = os.path.abspath(
            os.path.dirname(os.path.realpath(sys.argv[0]))
        )
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
        self._config = config

    def get_public_ip(self):
        with requests.Session() as s:
            r = s.get("https://nstool.netease.com/", headers=self._headers)
            src_url = re.findall(r"src='(.*?)'", r.text)[0]
            r = s.get(src_url, headers=self._headers).text
            ip = re.findall(r"您的IP地址信息: (.*?) ", r)[0]
            ip_location = re.findall(r"您的IP地址信息: .*? (.*?)<br>", r)[0]
            print("公网IP地址：" + ip)
            print("公网IP地址所在地：" + ip_location)

    def get_dns_address(self):
        with requests.Session() as s:
            r = s.get("https://nstool.netease.com/", headers=self._headers)
            src_url = re.findall(r"src='(.*?)'", r.text)[0]
            r = s.get(src_url, headers=self._headers).text
            if "您的DNS设置正确" in r:
                dns_address = re.findall(r"您的DNS地址信息: (.*?) ", r)[0]
                dns_address_location = re.findall(
                    r"您的DNS地址信息: .*? (.*?)<br>", r
                )[0]
                print("DNS地址：" + dns_address)
                print("DNS地址所在地：" + dns_address_location)
            else:
                print("DNS设置错误！")

    def __check_internet_connection(self):
        if os.name == "nt":
            exit_code = os.system("ping www.baidu.com -w 1000 -n 1 > nul")
        elif os.name == "posix":
            exit_code = os.system("ping www.baidu.com -W 1 -c 1 > /dev/null")
        else:
            print("未知系统！请自行修改代码后运行！")
            exit(1)
        if exit_code == 0:
            self.__internet_connectivity = True
        else:
            self.__internet_connectivity = False

    def login(self):
        self.__check_internet_connection()
        if self.__internet_connectivity:
            print(
                "网络已连接！", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
        else:
            print(
                "网络未连接！", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            print(
                "尝试登录...", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            )
            self._login_function()

    def login_auto(self):
        sleep_time = input("请输入自动检测间隔时间(单位：分钟):")
        print("程序将每隔" + sleep_time + "分钟自动检测网络连接状态并登录!")
        print("按下Ctrl+C可退出程序!")
        while True:
            self.login()
            time.sleep(60 * int(sleep_time))

    def _login_function(self):
        raise NotImplementedError


class DrcomSzuDormitory(DrcomSzu):
    def __init__(self):
        super().__init__()

    def __get_ip(self):
        r = requests.get("http://172.30.255.42", headers=self._headers).text
        ip = re.findall(r"v46ip='(.*?)'", r)[0]
        print("校内IP地址：" + ip)
        return ip

    def _login_function(self):
        payload = {
            "callback": "dr1003",
            "login_method": "1",
            "user_account": ",0," + self._config["username"],
            "user_password": self._config["password"],
            "wlan_user_ip": self.__get_ip(),
            "wlan_user_ipv6": "",
            "wlan_user_mac": "000000000000",
            "wlan_ac_ip": "",
            "wlan_ac_name": "",
            "jsVersion": "4.1.3",
            "terminal_type": "1",
            "lang": "en",
            "v": "3246",
            "lang": "en",
        }
        drcom_res = requests.get(
            "http://172.30.255.42:801/eportal/portal/login",
            params=payload,
            headers=self._headers,
        )
        result = re.findall(r"\"result\":(\d)", drcom_res.text)[0]
        if result == "1":
            print("登录成功！")
        elif result == "0":
            print("登录失败！")


class DrcomSzuOffice(DrcomSzu):
    def __init__(self):
        super().__init__()

    def _login_function(self):
        drcom_form = {
            "DDDDD": self._config["username"],
            "upass": self._config["password"],
            "0MKKey": "%B5%C7%A1%A1%C2%BC",
        }
        drcom_res = requests.post(
            "https://drcom.szu.edu.cn/a70.htm",
            data=drcom_form,
            headers=self._headers,
        )
        title = re.findall(r"<title>(.*?)</title>", drcom_res.text)[0]
        if title == "Drcom PC登陆成功页":
            print("登录成功！")
        else:
            print("登录失败！")


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
            "5. 查询公网ip\n"
            "6. 查询DNS地址\n"
            "100. 退出程序\n"
            "请输入功能编号："
        )
        print("----------------------------------------")
        match type:
            case "0":
                DrcomSzu.set_config()
            case "1":
                drcom_login(DrcomSzuDormitory(), False)
            case "2":
                drcom_login(DrcomSzuOffice(), False)
            case "3":
                drcom_login(DrcomSzuDormitory(), True)
            case "4":
                drcom_login(DrcomSzuOffice(), True)
            case "5":
                DrcomSzu().get_public_ip()
            case "6":
                DrcomSzu().get_dns_address()
            case "100":
                break
            case _:
                print("输入错误！请重新输入！")
        print("----------------------------------------")
        print("回车键继续...")
        input()
        if os.name == "nt":
            os.system("cls")
        elif os.name == "posix":
            os.system("clear")
        else:
            print("未知系统！无法清屏！")


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
        sys.exit()
