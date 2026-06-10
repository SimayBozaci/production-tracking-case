from fastapi import FastAPI, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware

import pandas as pd
import os
def safe_get(row, *keys, default=""):
    for k in keys:
        if k in row and pd.notna(row[k]):
            return row[k]
    return default
from database.models import (
    Upload,
    ValidationError,
    ProductionRecord
)
from database.database import engine
from database.database import Base
from database.database import SessionLocal




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

    df = pd.read_csv(file_path, encoding="cp1254")
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace("\n", "", regex=True)

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
        for _, row in df.iterrows():

            record = ProductionRecord(
                record_id=str(row.get("record_id", "")),
                tarih=str(row.get("Tarih", "")),
                vardiya=str(row.get("Vardiya", "")),
                is_istasyonu=safe_get(row, "İş İstasyonu", "Is Istasyonu"),
                stok_adi=str(row.get("Stok Adı", row.get("Stok Adi", ""))),
                oee=str(row.get("OEE", 0)),
                uretilen_miktar=str(row.get("Üretilen Miktar", 0)),
                hatali_uretilen_miktar=str(row.get("Hatalı Üretilen Miktar", 0)),
                upload_id=upload_record.id
            )

        db.add(record)

        for error in validation_result["errors"]:

            for error_detail in error["errors"]:

                validation_error = ValidationError(
                    upload_id=upload_record.id,
                    row_number=error["row"],
                    field_name=error_detail["field_name"],
                    error_type=error_detail["error_type"],
                    error_message=error_detail["error_message"],
                    action=error_detail["action"]
                )

                db.add(validation_error)

        db.commit()

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

@app.post("/sync-data")
def sync_data():

    db = SessionLocal()

    try:

        uploads = (
            db.query(Upload)
            .filter(
                Upload.validation_status == "PASSED"
            )
            .all()
        )

        total_records = sum(
            upload.valid_rows or 0
            for upload in uploads
        )

        return {
            "status": "SUCCESS",
            "uploaded_files": len(uploads),
            "sent_records": total_records,
            "message": "Valid records sent to target system"
        }

    finally:
        db.close()

@app.get("/validation-errors")
def get_validation_errors():

    db = SessionLocal()

    try:

        errors = (
            db.query(ValidationError)
            .order_by(
                ValidationError.id.desc()
            )
            .all()
        )

        return [
              {
                "id": error.id,
                "upload_id": error.upload_id,
                "row_number": error.row_number,
                "field_name": error.field_name,
                "error_type": error.error_type,
                "error_message": error.error_message,
                "action": error.action
            }
            for error in errors
        ]

    finally:
        db.close()
 
@app.get("/records")
def get_records(
    vardiya: str = Query(None),
    is_istasyonu: str = Query(None),
    stok_adi: str = Query(None)
):

    db = SessionLocal()

    try:

        query = db.query(ProductionRecord)

        if vardiya:
            query = query.filter(
                ProductionRecord.vardiya == vardiya
            )

        if is_istasyonu:
            query = query.filter(
                ProductionRecord.is_istasyonu == is_istasyonu
            )

        if stok_adi:
            query = query.filter(
                ProductionRecord.stok_adi.contains(stok_adi)
            )

        records = query.all()

        return [
            {
                "record_id": r.record_id,
                "tarih": r.tarih,
                "vardiya": r.vardiya,
                "is_istasyonu": r.is_istasyonu,
                "stok_adi": r.stok_adi,
                "oee": r.oee,
                "uretilen_miktar": r.uretilen_miktar,
                "hatali_uretilen_miktar": r.hatali_uretilen_miktar
            }
            for r in records
        ]

    finally:
        db.close()