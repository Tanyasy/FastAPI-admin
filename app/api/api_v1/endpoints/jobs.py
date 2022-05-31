import datetime
import time
from aioredis import Redis
import pickle

from fastapi import APIRouter, Depends, HTTPException, Body
from apscheduler.schedulers.background import BackgroundScheduler

from app.core.redis_pool import RedisPool
from app.api.utils.db import get_scheduler, get_redis
from app.schemas.reponse import BasicResponse, PageResponse
from app.api.utils.page import pagination
from app import scheduler
from app.core.logger import logger

router = APIRouter()


def time_format(timestamp: int) -> str:
    if timestamp < 60:
        return f"{timestamp}秒后"
    elif 60<= timestamp < 60*60:
        return f"{timestamp//60}分后"
    elif 60*60 <= timestamp < 24*60*60:
        return f"{timestamp//(60*60)}小时后"
    elif 24*60*60 <= timestamp:
        return f"{timestamp//24*60*60}天后"


@router.get("/", response_model=PageResponse)
async def get_jobs(
        page: int = 0,
        limit: int = 10,
        redis: RedisPool = Depends(get_redis)
):
    """
    定时任务持久化在redis里面，通过redis获取所有定时任务信息
    :param scheduler_obj: 全局任务调度器对象
    :param job_id: 任务名称
    :return:
    """
    # 连接redis获取任务信息
    redis_client: Redis = redis.select_db(db=1)
    scheduler_time = await redis_client.zrange("apscheduler.run_times", 0, -1, withscores=True)
    scheduler_msg = await redis_client.hgetall("apscheduler.jobs")

    redis_client: Redis = redis.select_db(db=2)
    scheduler_status = await redis_client.hgetall("scheduler_status")
    result = []
    now_day = datetime.datetime.now().day
    now_time_stamp = time.time()
    for k, v in scheduler_status.items():
        if v == b"0":
            scheduler_status[k] = "failed"
        elif v == str(now_day).encode("utf-8"):
            scheduler_status[k] = "success"
        else:
            scheduler_status[k] = "waiting"
    tamp_time = {}
    for i in scheduler_time:
        tamp_time[i[0]] = time_format(int(i[1]-now_time_stamp))

    for key, val in scheduler_msg.items():
        job_msg = pickle.loads(val)
        result.append({
            "id": key.decode("utf-8"),
            "name": job_msg.get("name"),
            "next_time": tamp_time.get(key) if tamp_time.get(key) else "暂停中...",
            "status": scheduler_status.get(key)
        })

    return pagination(result, page, limit)


@router.post("/", response_model=BasicResponse, tags=["jobs"])
async def add_job(
        scheduler_obj: BackgroundScheduler = Depends(get_scheduler),
        job_id: str = Body(..., embed=True)
):
    """
    通过传入job_id执行对应的任务，是否需要避免重复执行，由每个任务自己决定，只执行，执行结果有其他接口获取
    :param scheduler_obj: 全局任务调度器对象
    :param job_id: 任务名称
    :return:
    """
    job_function = getattr(scheduler, job_id)
    if not job_function:
        raise HTTPException(status_code=400, detail="Parameter verification failed!!!")

    # 判断任务是否存在，存在的话，暂停重新执行
    # if scheduler_obj.get_job(job_id):
    #     scheduler_obj.remove_job(job_id)
    # 异步执行任务
    scheduler_obj.add_job(job_function)

    return {
        "status": 200,
        "msg": "任务以开始执行"
    }


@router.delete("/{job_id}", response_model=BasicResponse, tags=["jobs"])
async def add_job(
        job_id: str,
        scheduler_obj: BackgroundScheduler = Depends(get_scheduler)
):
    """
    通过传入job_id暂停对应的任务，
    :param scheduler_obj: 全局任务调度器对象
    :param job_id: 任务名称
    :return:
    """
    job_function = getattr(scheduler, job_id)
    if not job_function:
        raise HTTPException(status_code=400, detail="Parameter verification failed!!!")

    # 判断任务是否存在，存在的话，暂停任务
    if scheduler_obj.get_job(job_id):
        scheduler_obj.pause_job(job_id)

    return {
        "status": 200,
        "msg": job_id + "任务已暂停"
    }


@router.put("/{job_id}", response_model=BasicResponse, tags=["jobs"])
async def add_job(
        job_id: str,
        scheduler_obj: BackgroundScheduler = Depends(get_scheduler)
):
    """
    通过传入job_id恢复暂停的对应任务，
    :param scheduler_obj: 全局任务调度器对象
    :param job_id: 任务名称
    :return:
    """
    job_function = getattr(scheduler, job_id)
    if not job_function:
        raise HTTPException(status_code=400, detail="Parameter verification failed!!!")

    # 判断任务是否存在，存在的话，暂停任务
    if scheduler_obj.get_job(job_id):
        scheduler_obj.resume_job(job_id)

    return {
        "status": 200,
        "msg": job_id + "任务已恢复"
    }
