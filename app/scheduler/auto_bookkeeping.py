import time
import os
from datetime import datetime, timedelta
from typing import List
import re

import pyautogui
import pyperclip
import redis
import pandas as pd
import numpy as np

from app.scheduler import config
from app.core.logger import logger


class AutoBookkeeping:
    login_flag = False
    payment_open_flag = False

    def __init__(self):
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path = os.path.join(app_path, "image")
        self.data_path = os.path.join(app_path, "data")
        self.redis = redis.Redis(host="localhost", port=6379, db=2)

    def show_payment(self):
        """
        将账单显示在屏幕前方
        :return:
        """
        # 检查账单是否打开
        location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "payment.png"), confidence=0.9)

        if location:
            pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
            pyautogui.click(clicks=1)  # 点击
        else:
            # 否，检查微信是否以登录
            location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "weixin.png"), confidence=0.9)
            if location:
                pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
                pyautogui.click(clicks=1)  # 点击
                location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "login_weixin.png"),
                                                    confidence=0.9)
                if location:
                    pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
                    pyautogui.click(clicks=1)  # 点击
                    # 等待同步消息
                    time.sleep(10)
            else:
                # 登录微信
                self.login_weixin()
                # 等待同步消息
                time.sleep(10)
            self.open_payment()
            # 账单获取等待时间
            time.sleep(10)
        self.login_flag = True
        self.payment_open_flag = True

    def login_weixin(self):
        """
        登录微信
        :return:
        """
        pyautogui.keyDown("winleft")
        pyautogui.keyUp('winleft')

        # 点击微信
        pyautogui.moveTo((1275, 713), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

        # 点击登录
        pyautogui.moveTo((1280, 815), duration=0.5)
        pyautogui.click(clicks=1)

    def open_chrome(self):
        """
        打开chrome浏览器
        :return:
        """
        pyautogui.keyDown("winleft")
        pyautogui.keyUp('winleft')

        # 点击chrome
        pyautogui.moveTo((600, 913), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(1)
        # 最大化
        location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "max.png"), confidence=0.9)
        if location:
            pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
            pyautogui.click(clicks=1)  # 点击
            time.sleep(1)

        # 打开随手记网页
        pyautogui.moveTo((548, 103), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(3)

        pyautogui.moveTo((1209, 577), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

        pyautogui.moveTo((725, 60), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(1)

        # 判断当前输入法是否是中文输入
        location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "chinese.png"), confidence=0.9)
        if location:
            pyautogui.press("shiftleft")
            time.sleep(1)
        pyautogui.typewrite(self.data_path)
        pyautogui.keyDown("enter")
        pyautogui.keyUp('enter')

        pyautogui.moveTo((466, 639), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

        pyautogui.typewrite("new.xls")
        pyautogui.keyDown("enter")
        pyautogui.keyUp('enter')
        pyautogui.moveTo((984, 687), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

        # 上传数据
        pyautogui.moveTo((1270, 658), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(3)

        # 导入数据
        location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "import_data.png"), confidence=0.9)
        if location:
            pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
            pyautogui.click(clicks=1)  # 点击

        # 导入数据
        pyautogui.moveTo((1180, 734), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

    def open_payment(self):
        """
        打开账单，如果没打开的情况下
        :return:
        """
        # 点击登录
        pyautogui.moveTo((815, 400), duration=0.5)
        pyautogui.click(clicks=1)

        # 微信弹窗
        pyautogui.moveTo((1200, 1066), duration=0.5)
        pyautogui.click(clicks=1)

        # 统计
        pyautogui.moveTo((1195, 892), duration=0.5)
        pyautogui.click(clicks=1)

        # 等待
        time.sleep(3)

    def get_screen_msg(self, x1=1107, y1=607, x2=1514, y2=675) -> str:
        """
        截图指定区域的文字信息
        :return:
        """
        # 打开中键菜单
        pyautogui.click(x=1107, y=607, button='middle')

        # 打开utool截图工具
        location = pyautogui.locateCenterOnScreen(image=os.path.join(self.image_path, "shot.png"))
        pyautogui.moveTo(*location, duration=0.5)
        pyautogui.click(clicks=1)

        pyautogui.moveTo((x1, y1), duration=0.5)
        pyautogui.dragTo(x2, y2, duration=0.25)

        # 等待分析结果，关闭并复制
        time.sleep(3)
        pyautogui.moveTo((1702, 1063), duration=0.5)
        pyautogui.click(clicks=1)

        return pyperclip.paste()

    def get_date(self, day_name="yesterday.png"):
        if self.payment_open_flag:
            location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, day_name), confidence=0.9)
            if location:
                return True
            else:
                return False

    @staticmethod
    def format_str(raw_str: str) -> str:
        for idx, i in enumerate(raw_str):
            if i.isdigit():
                continue
            elif i == ":" or i == "|":
                continue
            else:
                break
        return raw_str[idx:]

    def format_data(self, row_str: str):
        str_list = row_str.split()
        if len(str_list) == 3:
            trade_type, money, backup = str_list
            backup = self.format_str(backup)
        elif len(str_list) == 4:
            trade_type, money, date_time, backup = str_list
        if money.startswith("-") or money.startswith("+"):
            money = money[1:]
        # print(f"{trade_type}, {money}, {backup}")
        return trade_type, money, backup

    def record_data(self):
        need_to_row: bool = self.get_date("today.png")

        out_list: List = []
        in_list: List = []
        yesterday: datetime = datetime.now() + timedelta(days=-1)
        yesterday_str: str = yesterday.strftime('%Y-%m-%d %I:%M:%S')
        while True:
            payment_str: str = self.get_screen_msg()
            # 当需要
            if "昨天" in payment_str:
                need_to_row: bool = False
                # 复位
                pyautogui.moveTo((1300, 700), duration=0.5)
                # 下移
                pyautogui.scroll(-94)
                continue
            if need_to_row:
                # 复位
                pyautogui.moveTo((1300, 700), duration=0.5)
                # 下移
                pyautogui.scroll(-94)
                continue
            if "出" in payment_str and not need_to_row:
                break
            trade_type, money, backup = self.format_data(payment_str)
            if trade_type in ["收红包", "商家转账", "退款"]:
                in_list.append({
                    "交易类型": "收入",
                    "日期": yesterday_str,
                    "分类": "收入",
                    "子分类": trade_type,
                    "账户1": "微信钱包",
                    "账户2": np.NAN,
                    "金额": money,
                    "成员": np.NAN,
                    "商家": np.NAN,
                    "项目": np.NAN,
                    "备注": backup,
                })
            else:
                out_list.append({
                    "交易类型": "支出",
                    "日期": yesterday_str,
                    "分类": "支出",
                    "子分类": trade_type,
                    "账户1": "微信钱包",
                    "账户2": np.NAN,
                    "金额": money,
                    "成员": np.NAN,
                    "商家": np.NAN,
                    "项目": np.NAN,
                    "备注": backup,
                })
            # 复位
            pyautogui.moveTo((1300, 700), duration=0.5)
            # 下移
            pyautogui.scroll(-94)

        # 判断是否有数据需要写入
        if len(out_list) == 0 and len(in_list) == 0:
            return 0

        data = pd.read_excel(os.path.join(self.data_path, 'temple.xls'), sheet_name=['支出', "收入"])
        out_df = data["支出"]
        in_df = data["收入"]

        out_df = out_df.append(out_list, ignore_index=True)
        in_df = in_df.append(in_list, ignore_index=True)

        # 将两个表格输出到一个excel文件里面
        writer = pd.ExcelWriter(os.path.join(self.data_path, 'new.xls'))
        out_df.to_excel(writer, sheet_name='支出', index=False, header=True)
        in_df.to_excel(writer, sheet_name='收入', index=False, header=True)

        # 必须运行writer.save()，不然不能输出到本地
        writer.save()

        return 1

    def get_image(self, x, y, width, height, name):
        im = pyautogui.screenshot(region=(x, y, width, height))
        im.save(os.path.join(self.image_path, f"{name}.png"))


# 首先考虑多种情况
# 1. 昨天没有消费：直接结束，不用记录
# 2. 昨天消费了，表还未更新： 直接走流程
# 3. 昨天消费了，表更新了，还未更新到记账本，更新处理
# 4. 都更新了，不用执行

def dump_data_to_excel():
    auto_keep = AutoBookkeeping()
    save_to_excel_flag = auto_keep.redis.get("save_to_excel")
    if save_to_excel_flag == b"1":
        logger.info("The data has been saved in excel，pass!!!!")
    elif save_to_excel_flag == b"0":
        logger.info("There was no consumption data yesterday and no need to update， pass!!!!")
    else:
        auto_keep.show_payment()
        save_to_excel_flag = auto_keep.record_data()
        # 写入标记
        auto_keep.redis.setex("save_to_excel", 12*60*60, save_to_excel_flag)
        logger.info("Save data to excel success")

    auto_keep.redis.close()


def save_data_to_cloud():
    auto_keep = AutoBookkeeping()
    save_to_cloud_flag = auto_keep.redis.get("save_to_cloud")
    if save_to_cloud_flag == b"1":
        logger.info("The task is successfully executed, pass!!!!")
    else:
        save_to_excel_flag = auto_keep.redis.get("save_to_excel")
        if save_to_excel_flag == b"1":
            auto_keep.open_chrome()
            # 写入标记
            auto_keep.redis.setex("save_to_cloud", 12 * 60 * 60, 1)
            logger.info("Save data to cloud success")
        elif save_to_excel_flag == b"0":
            logger.info("here was no consumption data yesterday, no need to save data to cloud，pass!!!!")
        else:
            logger.error("The Excel data is not updated, and the task fails to be executed")

    auto_keep.redis.close()


if __name__ == '__main__':
    dump_data_to_excel()
    # save_data_to_cloud()
    # auto_keep = AutoBookkeeping()
    # auto_keep.open_chrome()
    # auto_keep.show_payment()
    # save_to_excel_flag = auto_keep.record_data()
