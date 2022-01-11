from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Body
from apscheduler.schedulers.background import BackgroundScheduler

from app.api.utils.db import get_scheduler
from app.schemas.reponse import BasicResponse
from app import scheduler

router = APIRouter()


@router.post("/", response_model=BasicResponse, tags=["jobs"])
async def login_access_token(
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
    if scheduler_obj.get_job(job_id):
        scheduler_obj.remove_job()
    # 异步执行任务
    scheduler_obj.add_job(job_function, id=job_id)

    return {
        "status": 200,
        "msg": "任务以开始执行"
    }