from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database.database import Base


class Upload(Base):

    __tablename__ = "uploads"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    filename = Column(
        String,
        nullable=False
    )

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    row_count = Column(Integer)

    column_count = Column(Integer)

    status = Column(String)

    validation_status = Column(String)

    total_errors = Column(
        Integer,
        default=0
    )

    total_warnings = Column(
        Integer,
        default=0
    )

    valid_rows = Column(
        Integer,
        default=0
    )

    invalid_rows = Column(
        Integer,
        default=0
    )


class ValidationError(Base):

    __tablename__ = "validation_errors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    upload_id = Column(
        Integer,
        nullable=False
    )

    row_number = Column(
        Integer,
        nullable=False
    )

    field_name = Column(
        String,
        nullable=False
    )

    error_type = Column(
        String,
        nullable=False
    )

    error_message = Column(
        String,
        nullable=False
    )

    action = Column(
        String,
        default="REJECT"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


class ProductionRecord(Base):

    __tablename__ = "production_records"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    record_id = Column(String)

    tarih = Column(String)

    vardiya = Column(String)

    is_istasyonu = Column(String)

    stok_adi = Column(String)

    oee = Column(String)

    uretilen_miktar = Column(String)

    hatali_uretilen_miktar = Column(String)

    upload_id = Column(Integer)