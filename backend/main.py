from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os
import requests
from datetime import datetime
from database import get_db, create_tables, WeatherRecord
from models import WeatherRecordCreate, WeatherRecordUpdate
import json
import csv
import io
from fastapi.responses import StreamingResponse

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.on_event("startup")
def startup():
    create_tables()

@app.get("/")
def root():
    return {"msg": "Weather App Backend is running!"}

@app.get("/weather/current")
def get_current_weather(location: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Location not found")
    return response.json()

@app.get("/weather/forecast")
def get_forecast(location: str):
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Location not found")
    return response.json()

@app.post("/records")
def create_record(data: WeatherRecordCreate, db: Session = Depends(get_db)):
    try:
        date_from = datetime.strptime(data.date_from, "%Y-%m-%d")
        date_to = datetime.strptime(data.date_to, "%Y-%m-%d")
        if date_to < date_from:
            raise HTTPException(status_code=400, detail="End date must be after start date")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")

    url = f"http://api.openweathermap.org/data/2.5/weather?q={data.location}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="Location not found")
    
    weather = response.json()
    record = WeatherRecord(
        location=data.location,
        temperature=weather["main"]["temp"],
        description=weather["weather"][0]["description"],
        date_from=data.date_from,
        date_to=data.date_to,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record

@app.get("/records")
def get_records(db: Session = Depends(get_db)):
    return db.query(WeatherRecord).all()

@app.get("/records/{record_id}")
def get_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record

@app.put("/records/{record_id}")
def update_record(record_id: int, data: WeatherRecordUpdate, db: Session = Depends(get_db)):
    record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in data.dict(exclude_unset=True).items():
        setattr(record, key, value)
    db.commit()
    db.refresh(record)
    return record

@app.delete("/records/{record_id}")
def delete_record(record_id: int, db: Session = Depends(get_db)):
    record = db.query(WeatherRecord).filter(WeatherRecord.id == record_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    db.delete(record)
    db.commit()
    return {"msg": "Record deleted successfully"}

@app.get("/records/export/json")
def export_json(db: Session = Depends(get_db)):
    records = db.query(WeatherRecord).all()
    data = [{"id": r.id, "location": r.location, "temperature": r.temperature,
             "description": r.description, "date_from": r.date_from, "date_to": r.date_to} for r in records]
    return data

@app.get("/records/export/csv")
def export_csv(db: Session = Depends(get_db)):
    records = db.query(WeatherRecord).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "location", "temperature", "description", "date_from", "date_to"])
    for r in records:
        writer.writerow([r.id, r.location, r.temperature, r.description, r.date_from, r.date_to])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv",
                           headers={"Content-Disposition": "attachment; filename=weather_records.csv"})