from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import os

from database.database import engine
from database.database import Base
from database.database import SessionLocal

from database.models import Upload

from services.validation_service import validate_dataframe


app = FastAPI(title="Production Tracking API")

app.add_middleware(
    CORSMiddleware,
    # allow_origins=[
    #     "http://localhost:5174",
    #     "http://localhost:5173"
    # ],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.get("/")
def home():
    return {
        "message": "Production Tracking API Running"
    }


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):

    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    df = pd.read_csv(
        file_path,
        encoding="cp1254"
    )

    print(df.columns.tolist())

    validation_result = validate_dataframe(df)

    db = SessionLocal()

    try:

        upload_record = Upload(
            filename=file.filename,
            row_count=len(df),
            column_count=len(df.columns),
            status="VALIDATED",
            validation_status=(
                "PASSED"
                if validation_result["invalid_rows"] == 0
                else "FAILED"
            ),
            total_errors=validation_result["invalid_rows"],
            total_warnings=0,
            valid_rows=validation_result["valid_rows"],
            invalid_rows=validation_result["invalid_rows"]
        )

        db.add(upload_record)
        db.commit()
        db.refresh(upload_record)

        return {
            "upload_id": upload_record.id,
            "file_name": file.filename,
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "valid_rows": validation_result["valid_rows"],
            "invalid_rows": validation_result["invalid_rows"],
            "validation_status": upload_record.validation_status
        }

    finally:
        db.close()


@app.get("/uploads")
def get_uploads():

    db = SessionLocal()

    try:

        uploads = (
            db.query(Upload)
            .order_by(Upload.id.desc())
            .all()
        )

        return [
            {
                "upload_id": upload.id,
                "file_name": upload.filename,
                "row_count": upload.row_count,
                "column_count": upload.column_count,
                "status": upload.status,
                "validation_status": upload.validation_status,
                "valid_rows": upload.valid_rows,
                "invalid_rows": upload.invalid_rows
            }
            for upload in uploads
        ]

    finally:
        db.close()


@app.get("/report")
def get_report():

    db = SessionLocal()

    try:

        uploads = db.query(Upload).all()

        total_uploads = len(uploads)

        total_rows = sum(
            upload.row_count or 0
            for upload in uploads
        )

        total_valid_rows = sum(
            upload.valid_rows or 0
            for upload in uploads
        )

        total_invalid_rows = sum(
            upload.invalid_rows or 0
            for upload in uploads
        )

        validation_passed = len(
            [
                upload
                for upload in uploads
                if upload.validation_status == "PASSED"
            ]
        )

        validation_failed = len(
            [
                upload
                for upload in uploads
                if upload.validation_status == "FAILED"
            ]
        )

        return {
            "total_uploads": total_uploads,
            "total_rows": total_rows,
            "total_valid_rows": total_valid_rows,
            "total_invalid_rows": total_invalid_rows,
            "validation_passed": validation_passed,
            "validation_failed": validation_failed
        }

    finally:
        db.close()