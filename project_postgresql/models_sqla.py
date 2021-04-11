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
        doc='testtest',
    )
    app_label = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    model = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
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
        doc='testtest',
    )
    action_time = Column(
        postgresql_types.TIMESTAMP(),
        default=import_module('django.contrib.admin.models').LogEntry.action_time.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    content_type_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='django_content_type.id', ondelete='SET_NULL'),
        primary_key=False,
        unique=False,
        nullable=True,
        autoincrement=True,
        doc='testtest',
    )
    object_id = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    object_repr = Column(
        postgresql_types.VARCHAR(length=200),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    action_flag = Column(
        postgresql_types.SMALLINT(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    change_message = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    user = relationship(
        'User',
        primaryjoin='LogEntry.user_id == User.id',
        backref='logentry',
    )
    content_type = relationship(
        'ContentType',
        primaryjoin='LogEntry.content_type_id == ContentType.id',
        backref='logentry',
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
        doc='testtest',
    )
    group_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_group.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    permission_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_permission.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    group = relationship(
        'Group',
        primaryjoin='GroupPermissions.group_id == Group.id',
        backref='group_permissions',
    )
    permission = relationship(
        'Permission',
        primaryjoin='GroupPermissions.permission_id == Permission.id',
        backref='group_permissions',
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
        doc='testtest',
    )
    name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=True,
        nullable=False,
        doc='testtest',
    )
    permissions = relationship(
        'Permission',
        secondary='GroupPermissions',
        primaryjoin='Group.id == GroupPermissions.group_id',
        secondaryjoin='GroupPermissions.permission_id == Permission.id',
        backref='group',
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
        doc='testtest',
    )
    name = Column(
        postgresql_types.VARCHAR(length=255),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    content_type_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='django_content_type.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    codename = Column(
        postgresql_types.VARCHAR(length=100),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    content_type = relationship(
        'ContentType',
        primaryjoin='Permission.content_type_id == ContentType.id',
        backref='permission',
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
        doc='testtest',
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    group_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_group.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    user = relationship(
        'User',
        primaryjoin='UserGroups.user_id == User.id',
        backref='user_groups',
    )
    group = relationship(
        'Group',
        primaryjoin='UserGroups.group_id == Group.id',
        backref='user_groups',
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
        doc='testtest',
    )
    user_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_user.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    permission_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='auth_permission.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    user = relationship(
        'User',
        primaryjoin='UserUserPermissions.user_id == User.id',
        backref='user_user_permissions',
    )
    permission = relationship(
        'Permission',
        primaryjoin='UserUserPermissions.permission_id == Permission.id',
        backref='user_user_permissions',
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
        doc='testtest',
    )
    password = Column(
        postgresql_types.VARCHAR(length=128),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    last_login = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    is_superuser = Column(
        mysql_types.BOOLEAN(),
        default=import_module('django.contrib.auth.models').User.is_superuser.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    username = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=True,
        nullable=False,
        doc='testtest',
    )
    first_name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    last_name = Column(
        postgresql_types.VARCHAR(length=150),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    email = Column(
        postgresql_types.VARCHAR(length=254),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    is_staff = Column(
        mysql_types.BOOLEAN(),
        default=import_module('django.contrib.auth.models').User.is_staff.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    is_active = Column(
        mysql_types.BOOLEAN(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    date_joined = Column(
        postgresql_types.TIMESTAMP(),
        default=import_module('django.contrib.auth.models').User.date_joined.field.default,
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    groups = relationship(
        'Group',
        secondary='UserGroups',
        primaryjoin='User.id == UserGroups.user_id',
        secondaryjoin='UserGroups.group_id == Group.id',
        backref='user',
    )
    user_permissions = relationship(
        'Permission',
        secondary='UserUserPermissions',
        primaryjoin='User.id == UserUserPermissions.user_id',
        secondaryjoin='UserUserPermissions.permission_id == Permission.id',
        backref='user',
    )


class Session(Base):
    __tablename__ = 'django_session'
    __table_args__ = {'extend_existing': True}
    
    session_key = Column(
        postgresql_types.VARCHAR(length=40),
        primary_key=True,
        unique=True,
        nullable=False,
        doc='testtest',
    )
    session_data = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    expire_date = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )


class Author(Base):
    __tablename__ = 'author'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    name = Column(
        postgresql_types.VARCHAR(length=255),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    age = Column(
        postgresql_types.SMALLINT(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    email = Column(
        postgresql_types.VARCHAR(length=254),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )


class BookCategory(Base):
    __tablename__ = 'book_category'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    book_id = Column(
        postgresql_types.UUID(),
        ForeignKey(column='book.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    category_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='category.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    book = relationship(
        'Book',
        primaryjoin='BookCategory.book_id == Book.id',
        backref='book_category',
    )
    category = relationship(
        'Category',
        primaryjoin='BookCategory.category_id == Category.id',
        backref='book_category',
    )


class Book(Base):
    __tablename__ = 'book'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.UUID(),
        default=import_module('books.models').Book.id.field.default,
        primary_key=True,
        unique=True,
        nullable=False,
        doc='testtest',
    )
    price = Column(
        postgresql_types.JSONB(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    title = Column(
        postgresql_types.VARCHAR(length=255),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    description = Column(
        postgresql_types.TEXT(),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    author_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='author.id', ondelete='SET_NULL'),
        primary_key=False,
        unique=False,
        nullable=True,
        autoincrement=True,
        doc='testtest',
    )
    content = Column(
        postgresql_types.BYTEA(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    tags = Column(
        postgresql_types.ARRAY(item_type=postgresql_types.VARCHAR),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    author = relationship(
        'Author',
        primaryjoin='Book.author_id == Author.id',
        backref='books',
    )
    category = relationship(
        'Category',
        secondary='BookCategory',
        primaryjoin='Book.id == BookCategory.book_id',
        secondaryjoin='BookCategory.category_id == Category.id',
        backref='books',
        lazy='joined',
    )


class CategoryRelation(Base):
    __tablename__ = 'category_relation'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    category1_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='category.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    category2_id = Column(
        postgresql_types.INTEGER(),
        ForeignKey(column='category.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    type = Column(
        postgresql_types.VARCHAR(length=30),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    category1 = relationship(
        'Category',
        primaryjoin='CategoryRelation.category1_id == Category.id',
        backref='parents',
    )
    category2 = relationship(
        'Category',
        primaryjoin='CategoryRelation.category2_id == Category.id',
        backref='children',
    )


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.INTEGER(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    name = Column(
        original_types.CIText(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    created = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    related_coming = relationship(
        'Category',
        secondary='CategoryRelation',
        primaryjoin='Category.id == CategoryRelation.category1_id',
        secondaryjoin='CategoryRelation.category2_id == Category.id',
        backref='related_going',
    )


class Sales(Base):
    __tablename__ = 'sales'
    __table_args__ = {'extend_existing': True}
    
    id = Column(
        postgresql_types.BIGINT(),
        primary_key=True,
        unique=True,
        nullable=False,
        autoincrement=True,
        doc='testtest',
    )
    book_id = Column(
        postgresql_types.UUID(),
        ForeignKey(column='book.id', ondelete='CASCADE'),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    sold = Column(
        postgresql_types.TIMESTAMP(),
        primary_key=False,
        unique=False,
        nullable=False,
        doc='testtest',
    )
    reservation = Column(
        postgresql_types.INTERVAL(),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    source = Column(
        postgresql_types.INET(),
        primary_key=False,
        unique=False,
        nullable=True,
        doc='testtest',
    )
    book = relationship(
        'Book',
        primaryjoin='Sales.book_id == Book.id',
        backref='sales',
    )


