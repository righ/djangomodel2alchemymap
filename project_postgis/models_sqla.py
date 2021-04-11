from importlib import import_module

from sqlalchemy import (
    types as default_types,
    Column,
    ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import (
    postgresql as postgresql_types,
    mysql as mysql_types,
    oracle as oracle_types,
)
from d2a import original_types

try:
    from geoalchemy2 import types as geotypes
except ImportError:
    pass

Base = declarative_base()


class ContentType(Base):
    __tablename__ = 'django_content_type'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    app_label = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    model = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
    )


class LogEntry(Base):
    __tablename__ = 'django_admin_log'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    action_time = Column(
        postgresql_types.TIMESTAMP(),
        default=import_module('django.contrib.admin.models').LogEntry.action_time.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    content_type_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='django_content_type.id', ondelete='SET_NULL'),
        primary_key=False,
        unique=False,
        nullable=True,
        autoincrement=True,
    )
    object_id = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=True,
    )
    object_repr = Column(
        postgresql_types.VARCHAR(length=200),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    action_flag = Column(
        postgresql_types.SMALLINT(),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    change_message = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    user = relationship(
        'User',
        primaryjoin='LogEntry.user_id == User.id',
    )
    content_type = relationship(
        'ContentType',
        primaryjoin='LogEntry.content_type_id == ContentType.id',
    )


class GroupPermissions(Base):
    __tablename__ = 'auth_group_permissions'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    group_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_group.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    permission_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_permission.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    group = relationship(
        'Group',
        primaryjoin='GroupPermissions.group_id == Group.id',
    )
    permission = relationship(
        'Permission',
        primaryjoin='GroupPermissions.permission_id == Permission.id',
    )


class Group(Base):
    __tablename__ = 'auth_group'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=True,
        nullable=False,
    )
    permissions = relationship(
        'Permission',
        secondary='GroupPermissions',
        primaryjoin='Group.id == GroupPermissions.group_id',
        secondaryjoin='GroupPermissions.permission_id == Permission.id',
    )


class Permission(Base):
    __tablename__ = 'auth_permission'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    name = Column(
        postgresql_types.VARCHAR(length=255),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    content_type_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='django_content_type.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    codename = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    content_type = relationship(
        'ContentType',
        primaryjoin='Permission.content_type_id == ContentType.id',
    )


class UserGroups(Base):
    __tablename__ = 'auth_user_groups'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    group_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_group.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    user = relationship(
        'User',
        primaryjoin='UserGroups.user_id == User.id',
    )
    group = relationship(
        'Group',
        primaryjoin='UserGroups.group_id == Group.id',
    )


class UserUserPermissions(Base):
    __tablename__ = 'auth_user_user_permissions'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    permission_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_permission.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
    )
    user = relationship(
        'User',
        primaryjoin='UserUserPermissions.user_id == User.id',
    )
    permission = relationship(
        'Permission',
        primaryjoin='UserUserPermissions.permission_id == Permission.id',
    )


class User(Base):
    __tablename__ = 'auth_user'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    password = Column(
        postgresql_types.VARCHAR(length=128),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    last_login = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=True,
    )
    is_superuser = Column(
        mysql_types.BOOLEAN(),
        default=import_module('django.contrib.auth.models').User.is_superuser.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
    )
    username = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=True,
        nullable=False,
    )
    first_name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    last_name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    email = Column(
        postgresql_types.VARCHAR(length=254),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    is_staff = Column(
        mysql_types.BOOLEAN(),
        default=import_module('django.contrib.auth.models').User.is_staff.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
    )
    is_active = Column(
        mysql_types.BOOLEAN(),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    date_joined = Column(
        postgresql_types.TIMESTAMP(),
        default=import_module('django.contrib.auth.models').User.date_joined.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
    )
    groups = relationship(
        'Group',
        secondary='UserGroups',
        primaryjoin='User.id == UserGroups.user_id',
        secondaryjoin='UserGroups.group_id == Group.id',
    )
    user_permissions = relationship(
        'Permission',
        secondary='UserUserPermissions',
        primaryjoin='User.id == UserUserPermissions.user_id',
        secondaryjoin='UserUserPermissions.permission_id == Permission.id',
    )


class Session(Base):
    __tablename__ = 'django_session'
    __table_args__ = {'extend_existing': True}
    
    session_key = Column(
        postgresql_types.VARCHAR(length=40),
        primary_key=True,
        unique=True,
        nullable=False,
    )
    session_data = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    expire_date = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=False,
    )


class Address(Base):
    __tablename__ = 'addresses'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    detail = Column(
        postgresql_types.VARCHAR(length=255),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    geom = Column(
        geotypes.Geometry(geometry_type='POINT', srid=4326, dimension=2, spatial_index=True),
        primary_key=False,
        unique=False,
        nullable=False,
    )


class Lake(Base):
    __tablename__ = 'lakes'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
    )
    name = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
    )
    geom = Column(
        geotypes.Geometry(geometry_type='POLYGON', srid=4326, dimension=2, spatial_index=True),
        primary_key=False,
        unique=False,
        nullable=False,
    )


