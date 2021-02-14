from pydantic import BaseModel, Field
from typing import NewType
import types
from datetime import datetime
from app.crud.serializer_base import SerializerBase

from sqlalchemy import Integer


class RouterBaseModel(BaseModel):
    """这个类主要是给生成的schema增加操作"""
    class Config:
        orm_mode = True


def get_basemodel(cls):
    """通过读取model的信息，创建schema"""
    model_name = cls.__name__
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}

    for filed in cls.__table__.c:
        filed_name = str(filed).split('.')[-1]

        if filed.default:
            default_value = filed.default
        elif filed.nullable:
            default_value = ...
        else:
            default_value = None
        # 生成的结构： id:int=Field(...,)大概这样的结构
        res_field = Field(default_value, description=filed.description)  # Field参数

        if isinstance(filed.type, Integer):
            tp = NewType(filed_name, int)
        # elif isinstance(filed.type, datetime):
        #     tp = NewType(filed_name, datetime)
        else:
            tp = NewType(filed_name, str)
        __mappings__[filed_name] = {'tp': tp, 'Field': res_field}
    create_mapping = __mappings__.copy()
    create_mapping.pop("id")
    create_mapping.pop("create_time")
    create_mapping.pop("update_time")
    model = type(model_name, (RouterBaseModel,), __mappings__)
    create_model = type(model_name + "Create", (BaseModel,), create_mapping)
    serializer_class = SerializerBase[model, create_model, create_model]
    crud_model = types.new_class("CRUD" + model_name, (serializer_class,), {})
    # 将schema绑定到model
    cls.__model__ = crud_model
    return cls