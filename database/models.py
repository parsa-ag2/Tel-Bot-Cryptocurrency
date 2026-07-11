from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    BigInteger,
    DateTime,
    Text
)

from datetime import datetime

from database.db import Base



# =========================
# Admin Management
# مدیریت ادمین ها
# =========================

class Admin(Base):

    __tablename__ = "admins"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    telegram_id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )


    username = Column(
        String(100),
        nullable=True
    )


    added_by = Column(
        BigInteger,
        nullable=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# =========================
# Required Channels
# کانال های اجباری
# =========================

class RequiredChannel(Base):

    __tablename__ = "required_channels"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    channel_id = Column(
        BigInteger,
        unique=True,
        nullable=False
    )


    username = Column(
        String(100),
        nullable=True
    )


    title = Column(
        String(255),
        nullable=True
    )


    is_active = Column(
        Boolean,
        default=True
    )


    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )



# =========================
# Bot Settings
# تنظیمات کلی ربات
# =========================

class BotSetting(Base):

    __tablename__ = "bot_settings"


    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )


    key = Column(
        String(100),
        unique=True,
        nullable=False
    )


    value = Column(
        Text,
        nullable=True
    )


    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )