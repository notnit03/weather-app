# 🌤️ Weather App
Built by Nithya Vangala | PM Accelerator Technical Assessment

## About This Project
A full-stack weather application built with React.js (frontend) and Python FastAPI (backend). Users can search for real-time weather data, view 5-day forecasts, and save/manage weather records with full CRUD functionality.

## Features
- 🔍 Search weather by city, zip code, or coordinates
- 🌡️ Current weather with temperature, humidity, wind speed
- 📅 5-day weather forecast
- 💾 Save weather records to database
- ✏️ Edit and delete saved records
- 📤 Export records as CSV or JSON
- ⚠️ Error handling for invalid locations

## Tech Stack
- **Frontend:** React.js, Axios
- **Backend:** Python, FastAPI, SQLAlchemy
- **Database:** SQLite
- **API:** OpenWeatherMap API

## How to Run

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Environment Variables

### Backend (.env)
```
OPENWEATHER_API_KEY=your_api_key_here
```

### Frontend (.env)
```
REACT_APP_API_URL=http://127.0.0.1:8001
```

## API Endpoints
- GET /weather/current?location={city} - Get current weather
- GET /weather/forecast?location={city} - Get 5-day forecast
- POST /records - Save a weather record
- GET /records - Get all saved records
- PUT /records/{id} - Update a record
- DELETE /records/{id} - Delete a record
- GET /records/export/csv - Export as CSV
- GET /records/export/json - Export as JSON