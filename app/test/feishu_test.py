import time

import requests
import json
import cn2an
from typing import Dict


def get_access_token():
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {
        "Content-Type": "application/json; charset=utf-8"
    }
    app_id = "cli_a123d36c66f8d00b"
    app_secret = "lnnkwkSfV4FYOkI1jI8O9fHjnYZ6iW05"
    data = {
        "app_id": app_id,
        "app_secret": app_secret
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return json.loads(response.text).get("tenant_access_token")


def update_record(num: int, record: Dict) -> Dict:
    print(record)
    num_cn = cn2an.an2cn(str(num+1), "low")
    fields: Dict = record.get("fields")
    fields["标题"] = f"AIP饮食第{num_cn}天"
    fields["日期"] = int(round(time.time()*1000))
    if fields.get("不适感"):
        fields["不适感"] = []
    return {
        "fields": fields
    }


def get_last_record(table_id: str, app_token: str, headers: Dict) -> (int, Dict):
    record_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    result = requests.get(record_url, headers=headers)

    data = json.loads(result.text)["data"]
    return (data["total"], data['items'][-1])


def add_record(table_id: str, data: Dict, app_token: str, headers: Dict) -> None:
    record_url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records"
    result = requests.post(record_url, headers=headers, data=json.dumps(data))
    print(result.text)
    return json.loads(result.text).get("code")


def main():
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {get_access_token()}"
    }
    app_token = "bascniZRdNxF1JYZcqmWtPJSyxh"

    # table_id = "tblVp4Gum7lb9YlF"
    table_id = "tblFGJ2zhQn4hae7"
    print(headers)
    data = update_record(*get_last_record(table_id, app_token=app_token, headers=headers))
    print(data)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": f"Bearer {get_access_token()}"
    }
    return add_record(table_id, data, app_token=app_token, headers=headers)


if __name__ == '__main__':
    a = {}
    if not a:
        print("空")