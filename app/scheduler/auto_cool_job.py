import os
import time

from app.core.logger import logger
from app.scheduler.utils import recode_mission_result


def run_script(script_name="auto_cool.bat") -> int:
    """
    用于调用脚本，控制每天的电压力锅做饭
    :return:
    """
    # 调用脚本
    app_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    auto_cool_script = os.path.join(app_path, "scripts", script_name)
    os.system(auto_cool_script)
    logger.info("auto cool success")
    return 1


@recode_mission_result
def auto_cool_job() -> int:
    return run_script("auto_cool.bat")


def auto_cool_potatoes():
    run_script("自动煮饭.bat")
    time.sleep(60*21)
    run_script("自动煮饭.bat")


if __name__ == '__main__':
    auto_cool_potatoes()
    # auto_cool_job()
    # auto_cool_job("自动煮饭.bat")
    # time.sleep(60*21)
    # auto_cool_job("自动煮饭.bat")

