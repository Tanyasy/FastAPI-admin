from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.executors.pool import ThreadPoolExecutor

from app.scheduler.feishu_job import main


def init_scheduler():
    """初始化"""
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
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=job_stores, executors=executors, timezone='Asia/Shanghai')
    # 添加定时任务
    scheduler.add_job(main, 'cron', hour=14, minute=5, jobstore="redis")
    scheduler.start()
