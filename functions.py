import datetime
import random
import requests
import os
import platform

os_name = platform.system()

def replace_char(s, len_pwd):
    """
    强行对密码所在内存地址进行编辑。用于增强对密码的隐私保护功能。
    （python没有指针，真的是好难受呀，嘤嘤嘤～）
    输入值： 字符串、修改的位置
    返回值： 0
    """
    import ctypes
    OFFSET = ctypes.sizeof(ctypes.c_size_t) * 6
    a = ctypes.c_char.from_address(id(s) + OFFSET)
    pi = ctypes.pointer(a)
    for idx in range(len_pwd):
        pi[idx] = ord('*')
    return 0

def clearWindow():
    """
    根据操作系统，自动选择清屏方式
    输入值： 无
    返回值： 无
    """
    if os_name == 'Windows':
        os.system("cls")
    elif os_name == 'Linux':
        os.system("clear")
    else:
        raise Exception("未知操作系统，目前仅支持Linux和Windows，嘤～")

def getNowHourMinSec():
    """
    获取现在的时分秒
    输入值： 无
    返回值： 当前是时、分、秒，返回的形式是HOUR、MINIUTE、SECONDS
    """
    d = datetime.datetime.now()
    hour = int(str(d)[11:13])
    miniute = int(str(d)[14:16])
    seconds = int(str(d)[17:19])
    return hour, miniute, seconds

def updateTimeLib(time_lib):
    """
    随机更新下一天上报的时间
    输入值： 原来的上报时间
    返回值： 更新的上报时间
    """
    assert len(time_lib) == 6
    new_time = time_lib
    new_time[1] = random.randint(2,59)
    new_time[3] = random.randint(2,59)
    new_time[5] = random.randint(2,59)
    print("更新晨午晚检上报时间成功！下一天的上报时间为:")
    print("晨检 - %d点%d分，午检 - %d点%d分，晚检 - %d点%d分。" % tuple(new_time))
    return new_time

def checkTime(time_lib):
    """
    判断当前时刻是否需要上报，以及对应模式
    输入值： 上报时间
    返回值： 上报模式(1, 2, 3分别对应晨午晚检)
    """
    Hour, Minus, Secs = getNowHourMinSec()
    if Hour == time_lib[0] and Minus == time_lib[1]:
        # 晨检
        currentState = 1
    elif Hour == time_lib[2] and Minus == time_lib[3]:
        # 午检
        currentState = 2
    elif Hour == time_lib[4] and Minus == time_lib[5]:
        # 晚检
        currentState = 3
    elif Hour == 23 and Minus == 55:
        # 夜间模式
        currentState = 4
    elif not Minus:
        # 整点时刻
        currentState = 5
    else:
        currentState = 0
    if currentState:
        print("当前系统时间  %d:%d:%d" % (Hour, Minus, Secs))
    return currentState

def checkInternetConnection():
    try:
        requests.get("https://xxcapp.xidian.edu.cn/site/ncov/xisudailyup", timeout=5)
    except:
        return False
    return True

def getInfo():
    from utils.USER import COOKIE_FILE_NAME
    CONFIG_PATH = "./data/config.json"
    if os.path.exists(CONFIG_PATH):
        import json
        # 获取json文件内容
        config_file = open(CONFIG_PATH, 'r', encoding="utf-8")
        config = json.load(config_file)
    else:
        config = dict()
    # 之所以不直接判断不存在这个key就让填写，是因为怕用户不想填的时候没有删掉这个key，那就尴尬啦，嘤～
    for idx_key in ("stuNum", "passWord", "Location", "ServerToken"):
        if not (idx_key in config):
            config[idx_key] = 0
    # 补全缺失的信息
    if not config["stuNum"]:
        # 用户输入学号
        config["stuNum"] = input("请输入学号/工号，按回车键结束：")
        # 确认学号是合法的非0数字
        assert int(config["stuNum"], base=10)
    if not config["Location"]:
        # config["Location"] = input("选择想定位的地点：0：南校区，1：北校区，2：在校外，按回车键结束：")
        # 判断工号类型，老师/本科生/研究生
        if len(config["stuNum"]) < 8:
            # 教职工
            # 定位在哪个校区的事情，学校从来就不看，别写疫区就行，所以无所谓，随便给一个，解决你的选择困难症
            import random
            config["Location"] = random.randint(1,2)
            print("已自动识别您是教职工，随机定位在" + ("北校区" if config["Location"]==1 else "南校区"))
        elif int(config["stuNum"][4] == "1"):
            # 研究生
            school_id = int(config["stuNum"][2:4])
            if school_id in (1, 2, 3, 4, 5, 14, 17):
                # 通院，电院，计科，机电，物光，微电子，智能 --> 北校区
                config["Location"] = 1
                print("已自动识别您是硕士/博士生，定位在北校区")
            else:
                # 其他学院 --> 南校区
                config["Location"] = 2
                print("已自动识别您是硕士/博士生，定位在南校区")
        elif int(config["stuNum"][4] == "0"):
            # 本科生 --> 南校区
            config["Location"] = 2
            print("已自动识别您是本科生")
        else:
            # 无法识别学号/工号 --> 校外
            config["Location"] = 3
            print("系统无法识别您的身份，已自动定位到校外")
    if not(os.path.exists(COOKIE_FILE_NAME)):
        if not config["passWord"]:
            config["passWord"] = input("请输入密码，密码将明文显示，请注意遮挡键盘，按下回车键后将自动清屏：")
            # 清屏
            clearWindow()
    return config
