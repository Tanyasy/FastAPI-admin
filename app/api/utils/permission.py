from typing import List, Callable
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

from app.models.user import User
from app.api.utils.session import get_current_active_user
from app.api.utils.db import get_db
from app.models.role import Role


def func_user_has_permissions(need_permissions: List[str] = None) -> Callable:
    """
    生成权限认证的依赖
    """

    async def user_has_permission(user: User = Depends(get_current_active_user), db: Session = Depends(get_db),) -> User:
        """
        是否有某权限
        """
        if user.is_superuser:
            return user
        if not need_permissions:
            return user
        for need_permission in need_permissions:
            # role_permission是一个table对象，要通过c属性才能获取其表中的属性
            res = db.query(Role).filter(Role.id == user.role_id).first()

            if need_permission not in [permission.codename for permission in res.permissions]:
                raise HTTPException(status_code=403, detail="没有权限")
        return user

    return user_has_permission