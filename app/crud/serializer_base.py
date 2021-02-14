from typing import List, Optional, Generic, TypeVar, Type

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session
from fastapi import Depends, Path
from app.api.utils.db import get_db

# TypeVar定义一个泛型，类似于T，且可能类型是Base类或其子类
ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


# 自定义泛型类
class SerializerBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    @classmethod
    def api_model_type(cls) -> Type[ModelType]:
        # print(cls.__orig_bases__[0].__args__)
        return cls.__orig_bases__[0].__args__[0]

    @classmethod
    def api_create_type(cls) -> Type[CreateSchemaType]:

        return cls.__orig_bases__[0].__args__[1]

    @classmethod
    def api_update_type(cls) -> Type[UpdateSchemaType]:

        return cls.__orig_bases__[0].__args__[2]


    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def register(self, ul: str, route: APIRouter):
        """注册到路由"""
        api_model = self.api_model_type()
        # print(api_model)
        # print(self.model)
        api_create = self.api_create_type()
        api_update = self.api_update_type()

        @route.get(ul + "/{id}", response_model=api_model)
        def get(*, id: str = Path(..., title="The ID of the item to get"), db_session: Session = Depends(get_db)) -> Optional[api_model]:
            return db_session.query(self.model).filter(self.model.id == id).first()

        @route.get(ul, response_model=List[api_model])
        def get_multi(db_session: Session = Depends(get_db), *, skip=0, limit=100) -> List[ModelType]:
            return db_session.query(self.model).offset(skip).limit(limit).all()

        @route.post(ul, response_model=List[api_model])
        def create_multi(*, obj_in: List[api_create], db_session: Session = Depends(get_db)) -> List[
            ModelType]:
            obj_list_in_data = jsonable_encoder(obj_in)
            db_obj_list = [self.model(**obj_in_data) for obj_in_data in obj_list_in_data]
            db_session.add_all(db_obj_list)
            db_session.flush()
            db_session.commit()
            return db_obj_list

        @route.put(ul, response_model=List[api_model])
        def update(*, db_obj: ModelType, obj_in: api_update, db_session: Session = Depends(get_db)
        ) -> ModelType:
            obj_data = jsonable_encoder(db_obj)
            update_data = obj_in.dict(skip_defaults=True)
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            db_session.add(db_obj)
            db_session.commit()
            db_session.refresh(db_obj)
            return db_obj

        @route.delete(ul, response_model=api_model)
        def remove(*, id: str, db_session: Session = Depends(get_db)) -> ModelType:
            obj = db_session.query(self.model).get(id)
            db_session.delete(obj)
            db_session.commit()
            return obj

        return route

