from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from yfinance_api.routers import history, indicators, info, quote

app = FastAPI(title="YFinance API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(quote.router)
app.include_router(history.router)
app.include_router(info.router)
app.include_router(indicators.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
