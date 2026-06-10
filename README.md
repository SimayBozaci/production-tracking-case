# 📊 Production Tracking Dashboard

## Project Overview

This is a full-stack Production Tracking System developed for the MAGNA technical case study.

The application processes production CSV files, validates data quality using a rule-based engine, stores records in a database, provides KPI analytics via dashboard, and simulates external system synchronization.

The system demonstrates a complete data pipeline: ingestion → validation → storage → API → frontend visualization.

---

## Tech Stack

Frontend: React (Vite), Material UI  
Backend: FastAPI, SQLAlchemy, Pandas  
Database: SQLite  

---

## Architecture

CSV File → FastAPI → Validation Engine → SQLite → REST API → React Dashboard

---

## Features

- CSV file upload and processing
- Rule-based validation engine
- Row-level error tracking
- KPI dashboard (total, valid, invalid records)
- Upload history tracking
- Server-side filtering (vardiya, iş istasyonu, stok adı)
- Mock synchronization endpoint (/sync-data)

---

## Validation Rules

- Missing record_id check
- Duplicate record detection
- Invalid OEE values
- Negative production quantities
- Data consistency checks

---

## API Endpoints

POST /upload-csv  
GET /records  
GET /report  
GET /uploads  
GET /validation-errors  
POST /sync-data  

---

## Setup Instructions

### Backend
cd backend  
python -m venv venv  
source venv/bin/activate  
pip install -r requirements.txt  
uvicorn app:app --reload  

Backend runs on: http://127.0.0.1:8000  

Swagger: http://127.0.0.1:8000/docs  

---

### Frontend
cd frontend  
npm install  
npm run dev  

Frontend runs on: http://localhost:5173  

---

## Data Flow

CSV Upload → Validation Engine → Database → API → Frontend Dashboard

---

## Screenshots


All UI screenshots are stored under the `screenshots/` directory.


---

## Limitations

- External API integration is mocked
- No authentication layer
- No pagination implemented
- No advanced analytics charts

---

## Future Improvements

- Authentication & role-based access control
- Real external API integration
- Retry & idempotency mechanisms
- OEE trend charts
- Pagination & sorting
- Docker deployment
- PostgreSQL migration
- CI/CD pipeline

---

## Author

Simay Bozacı  
MAGNA Technical Case Study – Production Tracking System
