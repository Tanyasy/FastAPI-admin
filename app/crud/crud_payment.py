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
            db_session:Session,
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

            for index, row in format_data.iterrows():
                data.append({
                    "money": float(row["金额(元)"].replace("¥", "")),
                    "counter_party": row["交易对方"].strip(),
                    "payment": row["收/支"].strip(),
                    "product_name": row["商品"].strip(),
                    "trade_sources": row["支付方式"].strip(),
                    "trade_number": row["交易单号"].strip(),
                    "create_time": row["交易时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
                    "update_time": row["交易时间"].strip().replace(" ", "T").replace("/", "-") + ":00",
                })
        return data


payment = CRUBPayment(Payment)
