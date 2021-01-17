import requests
import json

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoiYWQxNDZhZWNjNWE3NDUzYTgzZWFhMDg0ODJjOGVhNDUiLCJleHAiOjE2MTE1MDQwMDIsInN1YiI6ImFjY2VzcyJ9.JLNV1cXNJVvt4xw64Isthz6vp5r-KmSjZyRUQJDBgpU"
url = "http://127.0.0.1:8080/api/v1/payments/"


data = [
    {
        "money": 1.20,
        "counter_party": "家乐缘",
        "payment": "支出",
        "product_name": "东莞-溪村F区-FA-1F-家乐缘-Z02554-餐线-美食餐线2号",
        "trade_sources": "其他（包括阿里巴巴和外部商家"
    }
]

headers = {
    "Authorization": f'Bearer {token}',
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.text)