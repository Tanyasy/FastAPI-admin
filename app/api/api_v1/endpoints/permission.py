from app.schemas.permission import Permission, PermissionCreate, PermissionUpdate
from app.models.permission import Permission as PermissionDB
from app.crud.serializer_base import SerializerBase
from fastapi import APIRouter


router = APIRouter()


class CRUDPermission(SerializerBase[Permission, PermissionCreate, PermissionUpdate]):
    pass

router = CRUDPermission(PermissionDB).register('/permission', router)