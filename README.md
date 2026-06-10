#  Production Tracking Dashboard

## Overview

Full-stack application that processes production CSV files, validates data quality, stores records, and visualizes KPIs through a dashboard.

---

## Tech Stack

Frontend: React (Vite), Material UI  
Backend: FastAPI, SQLAlchemy, Pandas  
Database: SQLite  

---

## Architecture

CSV Upload → FastAPI → Validation Engine → SQLite → React Dashboard

---

## Features

### CSV Upload
- Upload CSV files via API
- Automatic parsing with Pandas

### Validation Engine
- Missing fields check
- Duplicate record detection
- OEE & quantity validation rules
- Row-level error tracking

### Dashboard
- Total uploads
- Valid / invalid rows
- Validation status summary
- Production records table

### Filtering
- Shift (Vardiya)
- Work station
- Stock name
- Server-side filtering via API

### Sync Simulation
- `/sync-data` endpoint
- Processes only validated records

---

## API Endpoints

POST /upload-csv → Upload CSV file  
GET /records → Production records (with filters)  
GET /report → KPI summary  
GET /uploads → Upload history  
GET /validation-errors → Validation errors  
POST /sync-data → Sync simulation  

---

## Data Flow

CSV → Upload → Validation → Database → API → Frontend

---

## Setup

### Backend
cd backend  
pip install -r requirements.txt  
uvicorn app:app --reload  

### Frontend
cd frontend  
npm install  
npm run dev  

---

## Notes

- SQLite used for simplicity
- Sync endpoint is mocked
- No authentication (out of scope)
- Focus on full-stack pipeline + validation + dashboard

---

## Author

Simay Bozacı  
MAGNA Technical Case Study – Production Tracking System
