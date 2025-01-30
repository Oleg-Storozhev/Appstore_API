import uvicorn
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

from service.ml.metrics_calculator import MetricsCalculator
from service.ml.review_fetcher import ReviewFetcher

app = FastAPI()


@app.get("/healthcheck")
async def test():
    return JSONResponse(content={"message": "API is running!"})


@app.get("/get_reviews")
async def get_reviews(app_name: str, app_id: str):
    reviews = ReviewFetcher.fetch_reviews(app_name=app_name, app_id=app_id)
    metrics = MetricsCalculator.get_metrics(reviews)
    return JSONResponse(content={"reviews": reviews, "metrics": metrics})


@app.get("/download_reviews")
async def download_reviews(app_name: str):
    """Download raw review data as JSON."""
    reviews = {"example": "example"}
    file_path = "reviews.json"
    with open(file_path, "w") as f:
        json.dump(reviews, f)

    return FileResponse(file_path, filename="reviews.json")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
