import pickle
import requests
import os
import json

DEFAULT_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/84.0.4147.89",
    "X-Requested-With": "XMLHttpRequest"
}

LOGIN_URL = "https://xxcapp.xidian.edu.cn/uc/wap/login/check"

COOKIE_FILE_NAME = "data/cookie.inf"

def get_cookie_from_login(student_id: str, password: str, cookie_file_path=COOKIE_FILE_NAME):
    """
    登录获取cookie
    :param student_id: 学号
    :param password:  密码
    :param cookie_file_path cookies文件路径
    :return:
    """
    r = requests.post(LOGIN_URL, data={"username": student_id, "password": password}, headers=DEFAULT_HEADER)
    if r.status_code == 200:
        if r.json()['e'] == 0:
            print("登录成功，已为您自动开通免密支付，以后无需输入密码，嘤～")
            # 写入cookie文件，下次免密登录
            with open(cookie_file_path, 'wb') as f:
                pickle.dump(r.cookies, f)
            return r.cookies
        else:
            print(r.json()['m'])
            raise RuntimeError("登录失败, 请检查用户名或密码是否正确")


def load_cookie_from_file(cookie_file_path=COOKIE_FILE_NAME):
    """
    从文件中加载cookie
    :param cookie_file_path: 文件路径
    :return:
    """
    with open(cookie_file_path, 'rb') as f:
        return pickle.load(f)


def login(config):
    """
    登录的高阶API
    将登录操作的细节进行隐藏
    :return: _cookies 获得的cookies
    """
    _cookies = ""
    if os.path.exists(COOKIE_FILE_NAME):
        _cookies = load_cookie_from_file(COOKIE_FILE_NAME)
    else:
        stu_num = config["stuNum"]
        password = config["passWord"]
        _cookies = get_cookie_from_login(stu_num, password)
    return _cookies
