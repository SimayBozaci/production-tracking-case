from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime

from datetime import datetime

from database.database import Base


class Upload(Base):

    __tablename__ = "uploads"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    upload_time = Column(
        DateTime,
        default=datetime.utcnow
    )

    row_count = Column(Integer)

    column_count = Column(Integer)

    status = Column(String)

    validation_status = Column(String)

    total_errors = Column(Integer, default=0)

    total_warnings = Column(Integer, default=0)

    valid_rows = Column(Integer, default=0)

    invalid_rows = Column(Integer, default=0)