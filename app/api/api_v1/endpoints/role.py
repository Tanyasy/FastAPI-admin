from fastapi import APIRouter, Depends, Path, HTTPException
from typing import List
from sqlalchemy.orm import Session

from app.schemas.role import Role, RoleCreate, RoleUpdate
from app.schemas.permission import Permission
from app.models.permission import Permission as PermissionDB
from app.models.role import Role as RoleDB
from app.crud.serializer_base import SerializerBase
from app.api.utils.db import get_db


router = APIRouter()


class CRUDRole(SerializerBase[Role, RoleCreate, RoleUpdate]):
    pass


router = CRUDRole(RoleDB).register('/role', router)


@router.post("/role/{id}", response_model=Role)
async def role_add_permission(*,
        id: str = Path(..., min_length=32, max_length=32),
        permission_list: List[str],
        db: Session = Depends(get_db)
):
    # db_permission_list = []
    db_permission_list = db.query(PermissionDB).filter(PermissionDB.id.in_(permission_list)).all()
    role = db.query(RoleDB).filter(RoleDB.id == id).first()
    if not role:
        raise HTTPException(
            status_code=400,
            detail="The role id is not exists in the system.",
        )
    role.permissions = db_permission_list
    db.flush()
    db.commit()
    return role