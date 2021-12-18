import time
import requests
import json
import cn2an
import datetime
from typing import Dict, List

from app.scheduler import config
from app.core.logger import logger


def get_access_token() -> str:
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    data = {
        "app_id": config.APP_ID,
        "app_secret": config.APP_SECRET
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(response.text).get("tenant_access_token")


def get_last_record(table_id: str, headers: Dict) -> Dict:
    record_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config.APP_TOKEN}/tables/{table_id}/records"
    result = requests.get(record_url, headers=headers)
    data = json.loads(result.text)["data"]
    fields: Dict = data['items'][-1].get("fields")
    # 判断时间是否是当前日期
    today_time = int(time.mktime(datetime.date.today().timetuple())) * 1000
    if today_time <= fields["日期"]:
        # 大于当前日期直接返回
        return {}

    num_cn = cn2an.an2cn(str(data["total"]+1), "low")
    fields["标题"] = f"AIP饮食第{num_cn}天"
    fields["日期"] = int(round(time.time()*1000))
    if fields.get("不适感"):
        fields["不适感"] = []
    return {
        "fields": fields
    }


def add_record(table_id: str, data: Dict, headers: Dict) -> None:
    record_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{config.APP_TOKEN}/tables/{table_id}/records"
    result = requests.post(record_url, headers=headers, data=json.dumps(data))
    return json.loads(result.text).get("code")


def feishu_job() -> List:
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {get_access_token()}"
    }
    result = []
    for table_id in [config.MASTER_TABLE_ID, config.MEDICINE_TABLE_ID]:
        data = get_last_record(table_id, headers=headers)
        if not data:
            # data为空字典表示已经添加过数据，直接返回
            logger.warning(f"data already added, pass!!!!")
            continue
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "Authorization": f"Bearer {get_access_token()}"
        }
        result.append(add_record(table_id, data, headers=headers))
    logger.info(f"add data success")
    return result


if __name__ == '__main__':
    feishu_job()
