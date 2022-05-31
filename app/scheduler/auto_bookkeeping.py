import time
import os
from datetime import datetime, timedelta
from typing import List
import re
from selenium import webdriver

import pyautogui
import pyperclip
import redis
import pandas as pd
import numpy as np

from app.scheduler import config
from app.core.logger import logger
from app.scheduler.utils import recode_mission_result

class AutoBookkeeping:
    login_flag = False
    payment_open_flag = False

    def __init__(self):
        app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.image_path = os.path.join(app_path, "image")
        self.data_path = os.path.join(app_path, "data")
        self.redis = redis.Redis(host="localhost", port=6379, db=2, decode_responses=True)

    def show_payment(self):
        """
        将账单显示在屏幕前方
        :return:
        """
        # 检查账单是否打开
        if not self.__move_to_image("payment.png"):
            self.show_weixin()
            self.open_payment()
            self.__wait_show("payment_book.png", 5, 10, click="")

        self.login_flag = True
        self.payment_open_flag = True

    def wait_pulling(self, img="pulling.png"):
        time.sleep(5)
        while True:
            location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, img), confidence=0.9)
            if location:
                time.sleep(3)
            else:
                break

    def show_weixin(self):
        """
        显示微信界面
        :return:
        """
        # 否，检查微信是否以登录
        if self.__move_to_image("weixin.png"):
            if self.__move_to_image("login_weixin.png"):
                # 等待同步消息
                self.wait_pulling()
        else:
            # 登录微信
            self.login_weixin()
            # 等待同步消息
            self.wait_pulling()

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
        time.sleep(2)

        # 点击登录
        self.__move_to_image("login_weixin.png")

    def open_chrome(self):
        """
        打开chrome浏览器
        :return:
        """
        driver = webdriver.Chrome()
        driver.get("https://www.sui.com/data/standard_data_import.do")

        driver.maximize_window()

        driver.find_element_by_xpath('//*[@id="email"]').send_keys("18860013592")
        driver.find_element_by_xpath('//*[@id="pwd"]').send_keys("hj3562145")
        driver.find_element_by_xpath('//*[@id="loginSubmit"]').click()

        time.sleep(3)

        pyautogui.moveTo((1209, 577), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击

        pyautogui.moveTo((800, 60), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(1)
        # 先判断是否是讯飞输入法
        while True:
            location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, "xunfei.png"), confidence=0.9)
            if not location:
                pyautogui.hotkey('shiftleft', 'ctrlleft')
                time.sleep(1)
            else:
                break
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
        self.__move_to_image("import_data.png")

        # 导入数据
        pyautogui.moveTo((1180, 734), duration=0.5)  # 移动鼠标
        pyautogui.click(clicks=1)  # 点击
        time.sleep(10)
        driver.close()

    def open_payment(self):
        """
        打开账单，如果没打开的情况下，试三次
        :return:
        """
        for i in range(3):
            # 点击微信支付
            self.__wait_show("weixin_pay.png", start_wait=1)

            # 微信弹窗
            self.__wait_show("my_payment.png", start_wait=1)
            # 统计
            self.__wait_show("payment_statistics.png", start_wait=2)

            time.sleep(2)
            if self.__move_to_image("payment.png", click=""):
                break

    def close_payment(self):
        """
        关闭账单，如果打开的情况下
        :return:
        """
        # 检查账单是否打开
        self.__move_to_image("payment.png", click="right")
        self.__wait_show("close_window.png", start_wait=1)

    def get_screen_msg(self, x1=1040, y1=570, x2=1525, y2=657) -> str:
        """
        截图指定区域的文字信息
        :return:
        """
        # 打开中键菜单
        pyautogui.click(x=1107, y=607, button='middle')

        # 打开utool截图工具
        self.__wait_show("shot.png", start_wait=1)
        pyautogui.moveTo((x1, y1), duration=0.5)
        pyautogui.dragTo(x2, y2, duration=0.25)

        # 等待分析结果，关闭并复制
        if not self.__wait_show("copy_and_close.png"):
            return ""

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
        yesterday_flag: bool = self.get_date()
        month_first_day_flag: bool = False

        out_list: List = []
        in_list: List = []
        today: datetime = datetime.now()
        # 每个月首月记账单中间会夹一条统计数据，这是需要特殊处理下
        if today.day == 1:
            month_first_day_flag = True
        yesterday: datetime = today + timedelta(days=-1)
        yesterday_str: str = yesterday.strftime('%Y-%m-%d %I:%M:%S')
        while True:
            payment_str: str = self.get_screen_msg()
            if not payment_str:
                break
            # 当需要
            if not yesterday_flag:
                return 0

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
            try:
                trade_type, money, backup = self.format_data(payment_str)
            except:
                break
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

    def appointment(self):
        # 打开微信
        if self.__move_to_image("longhua_hospital.png"):
            self.__move_to_image("smart_hospital.png")
            self.__move_to_image("internet_hospital.png")
        else:
            self.show_weixin()
            self.__move_to_image("longhua_hospital.png")
            self.__move_to_image("smart_hospital.png")
            self.__move_to_image("internet_hospital.png")
        self.__wait_show("my_appointment.png", start_wait=10, query_times=5)
        self.__wait_show("go_to_appointment.png", start_wait=5, query_times=8)
        self.__wait_show("already_read.png", start_wait=5)
        self.__wait_show("target_office_one.png", start_wait=5)
        self.__wait_show("target_office_two.png", start_wait=1)
        self.__wait_show("tomorrow.png", start_wait=5)
        self.__wait_show("afternoon.png", start_wait=1)
        self.__wait_show("alread_read_two.png", start_wait=4)

        self.__wait_show("first_gear.png", start_wait=4)
        # 选一档后查要一段时间，等个10s
        time.sleep(10)
        pyautogui.scroll(-500)
        self.__move_to_image("appointment_time.png")
        self.__wait_show("confirm.png", start_wait=10)

    def __move_to_image(self, image_name, click="left"):
        """
        移动至指定image中心位置，并点击
        :param image_name: 
        :return: 
        """
        location = pyautogui.locateOnScreen(image=os.path.join(self.image_path, image_name),
                                            confidence=0.95)
        if location:
            if click == "":
                return pyautogui.center(location)
            pyautogui.moveTo(*pyautogui.center(location), duration=0.5)  # 移动鼠标
            if click == "left":
                pyautogui.click(clicks=1)  # 点击
            elif click == "right":
                pyautogui.rightClick()
            elif click == "middle":
                pyautogui.middleClick()
            return pyautogui.center(location)
        logger.warning(f"{image_name} not found")

    def __wait_show(self, img="copy_and_close.png", start_wait=2, query_times=4, click="left"):
        time.sleep(start_wait)
        for i in range(query_times):
            if result := self.__move_to_image(img, click=click):
                return result
            else:
                time.sleep(1)
                continue
        logger.warning(f"can't not find {img}")



# 首先考虑多种情况
# 1. 昨天没有消费：直接结束，不用记录
# 2. 昨天消费了，表还未更新： 直接走流程
# 3. 昨天消费了，表更新了，还未更新到记账本，更新处理
# 4. 都更新了，不用执行


@recode_mission_result
def dump_data_to_excel():
    auto_keep = AutoBookkeeping()

    auto_keep.show_payment()
    save_to_excel_flag = auto_keep.record_data()

    auto_keep.close_payment()
    auto_keep.redis.close()
    return save_to_excel_flag


@recode_mission_result
def save_data_to_cloud():
    auto_keep = AutoBookkeeping()
    now_day = datetime.now().day
    save_to_excel_flag = auto_keep.redis.hget("scheduler_status", "dump_data_to_excel")
    match save_to_excel_flag:
        case str(now_day):
            auto_keep.open_chrome()
            logger.info("Save data to cloud success")
            return 1
        case "0":
            logger.info("here was no consumption data yesterday, no need to save data to cloud，pass!!!!")
            return 1
        case _:
            logger.error("The Excel data is not updated, and the task fails to be executed")

    auto_keep.redis.close()


if __name__ == '__main__':
    dump_data_to_excel()
    # save_data_to_cloud()
    # auto_keep = AutoBookkeeping()
    # auto_keep.open_chrome()
    # auto_keep.appointment()
    # auto_keep.close_payment()
    # auto_keep.show_payment()
    # save_to_excel_flag = auto_keep.record_data()
    # auto_keep.close_payment()
    # auto_keep.open_chrome()

