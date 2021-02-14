from sqlalchemy import Column, String, Integer, ForeignKey, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db.base_class import Base, get_id
from app.models.role import Role


role_permission = Table(
    'role_permission',
    Base.metadata,
    Column("id", String(32), primary_key=True, index=True, default=get_id),
    Column("role_id", String(64), ForeignKey("role.id")),
    Column("permission_id", String(100), ForeignKey("permission.id")),
    # 添加多列唯一约束，
    UniqueConstraint('role_id', 'permission_id', name='idx_role_id_permission_id'),
)


class Permission(Base):
    name = Column(String(128), unique=True, index=True, comment="权限名称")  # 权限名称
    codename = Column(String(100), comment="权限字段")  # 权限字段,也是我们平判断权限输入的字段
    roles = relationship(Role, backref="permissions", secondary=role_permission)