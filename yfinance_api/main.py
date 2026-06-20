from fastapi import FastAPI

from yfinance_api.routers import history, info, quote

app = FastAPI(title="YFinance API", version="0.1.0")

app.include_router(quote.router)
app.include_router(history.router)
app.include_router(info.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
