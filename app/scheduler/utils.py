import redis
import datetime
from functools import wraps

from app.core.logger import logger

store = redis.Redis(host="localhost", port=6379, db=2, decode_responses=True)
now_day = datetime.datetime.now().day


def recode_mission_result(function):

    @wraps(function)
    def inner():
        try:
            function_name = function.__name__
            logger.info(f"start {function_name} ..........")
            result = store.hget("scheduler_status", function_name)
            logger.info(f"{function_name} scheduler_status is {result}")
            if result == str(now_day):
                logger.info(f"{function_name} been done，pass!!!!")
            # elif result == b"0":
            #     logger.info(f"{function_name} excel failed，pass!!!!")
            else:
                result = function()
                if result:
                    store.hset("scheduler_status", function_name, now_day)
                else:
                    store.hset("scheduler_status", function_name, 0)
                return result
        except:
            logger.info(f"{function.__name__} failed")
            store.hset("scheduler_status", function.__name__, 0)

    return inner
