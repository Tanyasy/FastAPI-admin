from fastapi import APIRouter, Depends, Path, HTTPException, Body
from typing import List
from sqlalchemy.orm import Session

from app.schemas.role import Role, RoleCreate, RoleUpdate, RoleCreateOrUpdate
from app.schemas.permission import Permission
from app.models.permission import Permission as PermissionDB
from app.models.role import Role as RoleDB
from app.crud.serializer_base import SerializerBase
from app.api.utils.db import get_db


router = APIRouter()


class CRUDRole(SerializerBase[Role, RoleCreate, RoleUpdate]):
    pass


router = CRUDRole(RoleDB).register('/role', router)


@router.post("/role/one", response_model=Role)
async def role_add_permission(*,
        role_in: RoleCreateOrUpdate,
        db: Session = Depends(get_db)
):
    # db_permission_list = []
    db_permission_list = db.query(PermissionDB).filter(PermissionDB.id.in_(role_in.permissions)).all()
    if role_in.id:
        role = db.query(RoleDB).filter(RoleDB.id == role_in.id).first()
        if not role:
            raise HTTPException(
                status_code=400,
                detail="The role id is not exists in the system.",
            )
        role.permissions = db_permission_list
        role.name = role_in.name
    else:
        role = RoleDB(name=role_in.name)
        role.permissions = db_permission_list
        db.add(role)
    db.flush()
    db.commit()
    return role