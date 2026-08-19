# StockEdge Development Setup

This document describes how to run the current StockEdge prototype locally.

## Prerequisites

- Python 3.13 or a compatible Python version
- Node.js and npm
- The backend virtual environment created at `backend/venv`
- Frontend dependencies installed with `npm install`

## Start the backend

Open a PowerShell terminal and run:

```powershell
Set-Location "C:\Users\Jai\OneDrive\Desktop\Stock-edge\backend"
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

The backend API is available at:

- `http://localhost:8000/`
- `http://localhost:8000/docs` for FastAPI's interactive API documentation

The backend command should be started from the `backend` directory. The old `main:app` entry point remains as a compatibility wrapper, but new development commands should use `app.main:app`.

## Start the frontend

Open a second PowerShell terminal and run:

```powershell
Set-Location "C:\Users\Jai\OneDrive\Desktop\Stock-edge\frontend"
npm install
npm run dev -- --host 127.0.0.1
```

The React application is available at:

- `http://localhost:5173/`

The frontend calls the backend on port 8000. Both processes must be running for stock analysis to work.

## Useful checks

```powershell
Invoke-WebRequest -UseBasicParsing http://localhost:8000/
Invoke-WebRequest -UseBasicParsing http://localhost:8000/symbols
Invoke-WebRequest -UseBasicParsing http://localhost:5173/
```

To stop either development server, focus its terminal and press `Ctrl+C`.

## Notes

- `/` on port 8000 is the API health message, not the React page.
- The React page is served on port 5173.
- `/analyze/{symbol}` uses live Yahoo Finance data and may take several seconds.
- Do not commit `backend/venv`, `node_modules`, generated caches, or `.env` files.
