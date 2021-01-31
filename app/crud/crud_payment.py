from typing import List
from sqlalchemy.orm import Session, load_only, joinedload
from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from fastapi.encoders import jsonable_encoder
from datetime import datetime
import pandas as pd

from app.crud.base import CRUDBase
from app.models.payment import Payment
from app.models.trade_type import TradeType
from app.schemas.payment import PaymentCreate, PaymentUpdate


class CRUBPayment(CRUDBase[Payment, PaymentCreate, PaymentUpdate]):

    def get_multi_by_owner(
            self,
            db_session: Session,
            *,
            start_time: datetime = None,
            end_time: datetime = None,
            counter_party: str = None,
            product_name: str = None,
            trade_type: str = None,
            owner_id: str
    ) -> List[Payment]:

        # 根据传入的参数有无添加不同的过滤条件
        filter_conditions: list = [Payment.user_id == owner_id]
        if start_time:
            filter_conditions.append(Payment.create_time >= str(start_time))

        if end_time:
            filter_conditions.append(Payment.create_time <= str(end_time))

        if counter_party:
            filter_conditions.append(Payment.counter_party.like(f"%{counter_party}%"))

        if product_name:
            filter_conditions.append(Payment.product_name.like(f"%{product_name}%"))

        if trade_type:
            if trade_type == "null":
                filter_conditions.append(Payment.trade_type == None)
            else:
                filter_conditions.append(Payment.trade_type == trade_type)
        # 默认按时间降序排序，要在limit和offset之前，不然会报错
        return (
            db_session.query(self.model).options(joinedload("type").load_only("type_name", "type_flag"))
                .filter(and_(*filter_conditions))
                .order_by(Payment.create_time.desc())
                .all()
        )

    def create_multi_by_owner(self, db_session: Session, *, obj_in: List[PaymentCreate], owner_id: str) -> List[
        Payment]:
        obj_list_in_data = jsonable_encoder(obj_in)
        db_obj_list = [self.model(**obj_in_data, user_id=owner_id) for obj_in_data in obj_list_in_data]
        try:
            db_session.add_all(db_obj_list)
            db_session.flush()
            db_session.commit()
            return db_obj_list
        except IntegrityError as e:
            db_session.rollback()
            return []

    def update_multi(
            self,
            db_session: Session,
            *,
            obj_in: List[PaymentUpdate]
    ):
        obj_data = jsonable_encoder(obj_in)
        print(obj_data)
        db_session.bulk_update_mappings(self.model, obj_data)
        db_session.flush()
        db_session.commit()
        return obj_data

    @staticmethod
    def parse_xml_data(file_path: str, data_source: str) -> List[PaymentCreate]:

        data: list = []
        if data_source == "alipay":
            data_frame: pd.DataFrame = pd.read_csv(file_path, encoding="GBK")
            data_frame = data_frame.rename(columns=lambda x: x.strip())
            # 筛选冗余数据
            format_data: pd.DataFrame = data_frame[
                (data_frame["收/支"].apply(lambda x: not str(x).isspace())) & (data_frame["成功退款（元）"] == 0)]

            for index, row in format_data.iterrows():
                data.append({
                    "money": row["金额（元）"],
                    "counter_party": row["交易对方"].strip(),
                    "payment": row["收/支"].strip(),
                    "product_name": row["商品名称"].strip(),
                    "trade_sources": row["交易来源地"].strip(),
                    "trade_number": row["交易号"].strip(),
                    "create_time": row["交易创建时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
                    "update_time": row["最近修改时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
                })

        elif data_source == "weixinpay":
            data_frame: pd.DataFrame = pd.read_csv(file_path)
            data_frame = data_frame.rename(columns=lambda x: x.strip())
            # 筛选冗余数据
            format_data: pd.DataFrame = data_frame[(data_frame["收/支"].apply(lambda x: str(x) != "/"))]

            time_addition: str = ""
            if len(format_data["交易时间"][0].split(":")) == 2:
                time_addition = ":00"
            for index, row in format_data.iterrows():
                data.append({
                    "money": float(row["金额(元)"].replace("¥", "").replace(",", "")),
                    "counter_party": row["交易对方"].strip(),
                    "payment": row["收/支"].strip(),
                    "product_name": row["商品"].strip(),
                    "trade_sources": row["支付方式"].strip(),
                    "trade_number": row["交易单号"].strip(),
                    "create_time": row["交易时间"].strip().replace(" ", "T").replace("/", "-") + time_addition,
                    "update_time": row["交易时间"].strip().replace(" ", "T").replace("/", "-") + time_addition,
                })
        return data

    def get_statistics(self,
                       db_session: Session,
                       *,
                       start_time: datetime = None,
                       end_time: datetime = None,
                       owner_id: str,
                       select_date: str = None,
                       payment: str = None
                       ):
        records = self.get_multi_by_owner(
            db_session,
            start_time=start_time,
            end_time=end_time,
            owner_id=owner_id
        )
        encode_records: List[dict] = jsonable_encoder(records)
        # format_data: list = []
        for item in encode_records:
            trade_type: dict = item.pop("type")
            if trade_type:
                item["type_flag"] = trade_type.get("type_flag")
                item["type_name"] = trade_type.get("type_name")

        # 取指定列数据
        data_frame: pd.DataFrame = pd.DataFrame(encode_records,
                                                columns=["create_time", "money", "payment", "type_name", "type_flag"])

        # 筛选类型不为空的数据
        data_frame = data_frame[pd.notnull(data_frame["type_name"])]

        # 设置创建时间为索引，用于统计数据
        data_frame["create_time"] = pd.to_datetime(data_frame["create_time"])
        # 采用applay函数新增列，axis=1会将一行数据传入进行操作
        data_frame["int_out_money"] = data_frame.apply(lambda x: -x["money"] if x["payment"] == "支出" else x["money"], axis=1)
        data_frame = data_frame.set_index("create_time")

        if select_date:
            # 当select_date不为空时，表示查看详情
            data_frame = data_frame[select_date]
            if payment:
                if payment == "支出":
                    data_frame = data_frame[data_frame["type_flag"] < 100]
                else:
                    data_frame = data_frame[data_frame["type_flag"] >= 100]

            money_data: pd.Series = data_frame.groupby(["type_name"])["int_out_money"].sum()
            result = []
            for index, value in money_data.items():
                result.append(
                    {
                        "name": index,
                        "value": round(abs(value), 2)
                    }
                )
        else:
            # data_frame.groupby(["type_name"])["money"].sum()

            # 每个月的收支
            money_data: pd.Series = data_frame.to_period("m").groupby(["create_time", "payment"])["money"].sum()
            result = [["收/支", "支出", "收入"]]
            for index, value in money_data.items():
                if index[1] == "支出":
                    result.append([str(index[0]), round(value, 2)])
                else:
                    result[-1].append(round(value, 2))

        return result

        # 每个月每个种类的收支
        # data_frame.to_period("m").groupby(["create_time", "type_name"])["int_out_money"].sum()



payment = CRUBPayment(Payment)
