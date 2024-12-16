from fastapi import FastAPI
from .routes import scrapy_router as ScrapyRouter

app = FastAPI()
app.include_router(ScrapyRouter.router, tags=["ScrapyRuntime"], prefix="/scrapy")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this SheduleMatch domain !"}
