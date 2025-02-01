import uvicorn
import json
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

from service.connectors.mongodb_connector import MongoConnector
from service.ml.review_fetcher import ReviewFetcher
from service.metric_inference import MetricInference

app = FastAPI()
mongodb_connector = MongoConnector()
metric_inference = MetricInference()


@app.get("/healthcheck")
async def test():
    return JSONResponse(status_code=200,
                        content={"message": "API is running!"})


@app.post("/get_reviews")
async def get_reviews(app_name: str, app_id: str):
    reviews = ReviewFetcher.fetch_reviews(app_name=app_name, app_id=app_id)
    mongodb_connector.add_or_update_data(reviews)
    return JSONResponse(status_code=200,
                        content={"message": "Reviews fetched successfully."})


@app.get("/get_reviews_metrics")
async def get_reviews_metrics(app_name: str, app_id: str):
    reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)
    reviews_list = reviews["reviews"]
    result = metric_inference.run(reviews_list)
    metrics = result["metrics"]
    improvement_suggestions = result["improvement_suggestions"]

    return JSONResponse(status_code=200,
                        content={"metrics": metrics,
                                 "improvement_suggestions": improvement_suggestions
                                 })


@app.get("/download_reviews")
async def download_reviews(app_name: str, app_id: str):
    """Download raw review data as JSON."""
    reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)
    reviews_list = reviews["reviews"]
    file_path = f"reviews/{app_name}.json"
    with open(file_path, "w") as f:
        json.dump(reviews_list, f)

    return FileResponse(file_path, filename=f"{app_name}_reviews.json")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
