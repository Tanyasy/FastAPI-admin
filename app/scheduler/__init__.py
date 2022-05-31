import sys

from apscheduler.events import EVENT_JOB_ERROR, EVENT_JOB_MISSED, EVENT_JOB_EXECUTED
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import redis
import datetime
from functools import wraps

from app.scheduler.feishu_job import feishu_job
from app.scheduler.auto_cool_job import auto_cool_job, auto_cool_potatoes
from app.scheduler.auto_bookkeeping import dump_data_to_excel, save_data_to_cloud
from app.core.logger import logger


store = redis.Redis(host="localhost", port=6379, db=2, decode_responses=True)


def init_scheduler():
    """初始化"""
    def job_listener(Event):
        if not Event.exception:
            logger.info(f"jobname={Event.job_id}|jobtime={Event.scheduled_run_time}|retval={Event.retval}")
        else:
            logger.error(f"jobname={Event.job_id}|errcode={Event.code}|exception=[{Event.exception}]|traceback=[{Event.traceback}]|scheduled_time={Event.scheduled_run_time}",
                         )


    REDIS = {
        'host': '127.0.0.1',
        'port': '6379',
        'db': 1,
        'password': ''
    }
    job_stores = {
        'redis': RedisJobStore(**REDIS)  # SQLAlchemyJobStore指定存储链接
    }
    executors = {
        'default': ThreadPoolExecutor(10)  # 最大工作线程数20
        # 'processpool': ThreadPoolExecutor(max_workers=5)  # 最大工作进程数为5
    }

    job_defaults = {
        'coalesce': True,
        'max_instances': 3
    }

    scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
    scheduler.configure(jobstores=job_stores, executors=executors, job_defaults=job_defaults, timezone='Asia/Shanghai')

    scheduler.add_listener(job_listener, EVENT_JOB_ERROR | \
                           EVENT_JOB_MISSED | \
                           EVENT_JOB_EXECUTED)
    # 添加定时任务, replace_existing每次添加会覆盖之前的任务，设置id，每次启动任务都会重复添加一次，id随机
    scheduler.add_job(feishu_job, 'cron', hour=20, minute=8, misfire_grace_time=60*60*3, jobstore="redis",
                      replace_existing=True, id="feishu_job", name="飞书AIP饮食记录的添加")
    scheduler.add_job(auto_cool_job, 'cron', hour=22, minute=5, misfire_grace_time=60*60*3,
                      jobstore="redis", replace_existing=True, id="auto_cool_job", name="预约电压力锅早上做饭")

    # scheduler.add_job(dump_data_to_excel, 'cron', hour=12, minute=1, misfire_grace_time=60*60*3,
    #                   jobstore="redis", replace_existing=True, id="dump_data_to_excel", name="将微信昨天的账单导入到excel表格中")
    #
    # scheduler.add_job(save_data_to_cloud, 'cron', hour=22, minute=1, misfire_grace_time=60*60*3,
    #                   jobstore="redis", replace_existing=True, id="save_data_to_cloud", name="将excel账单上传到随手记中")

    scheduler.start()
    scheduler.print_jobs()
    now_day = datetime.datetime.now().day
    for job in scheduler.get_jobs():
        # 如果下次任务时间是下一天则判断是否执行成功了
        if job.next_run_time.day != now_day:
            # 获取执行结果
            if not store.hget("scheduler_status", job.id) or store.hget("scheduler_status", job.id) != str(now_day):

                scheduler.add_job(getattr(sys.modules[__name__], job.id))

    return scheduler

