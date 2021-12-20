import os
import time

from app.core.logger import logger


def auto_cool_job(script_name="auto_cool.bat") -> None:
    """
    用于调用脚本，控制每天的电压力锅做饭
    :return:
    """
    # 调用脚本
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    auto_cool_script = os.path.join(app_path, "scripts", script_name)
    os.system(auto_cool_script)
    logger.info("auto cool success")


if __name__ == '__main__':
    # auto_cool_job()
    auto_cool_job("自动煮饭.bat")
    # time.sleep(60*21)
    # auto_cool_job("自动煮饭.bat")
