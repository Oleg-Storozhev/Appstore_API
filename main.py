import json
import traceback
import uvicorn

from pydantic import BaseModel

from fastapi import Depends
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse

from service.connectors.mongodb_connector import MongoConnector
from service.metric_inference import MetricInference
from service.ml.review_fetcher import ReviewFetcher

app = FastAPI()


def get_mongo_connector():
    return MongoConnector()


def get_metric_inference():
    return MetricInference()


def validate_and_process_params(app_name: str, app_id: str):
    if not app_name:
        raise HTTPException(status_code=400, detail="The 'app_name' parameter is required.")
    if not app_id:
        raise HTTPException(status_code=400, detail="The 'app_id' parameter is required.")
    return app_name.lower(), app_id


class ReviewParams(BaseModel):
    app_name: str
    app_id: str


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "Something went wrong",
                 "exception": str(exc),
                 },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail,
                 "exception": str(exc)},
    )


@app.get("/healthcheck")
async def test():
    return JSONResponse(status_code=200,
                        content={"message": "API is running!"})


@app.post("/get_reviews")
async def get_reviews(
        params: ReviewParams,
        mongodb_connector: MongoConnector = Depends(get_mongo_connector)):

    app_name, app_id = params.app_name.lower(), params.app_id

    reviews = ReviewFetcher.fetch_reviews(app_name=app_name, app_id=app_id)
    if not reviews:
        raise HTTPException(status_code=404, detail="Reviews not found. Please check the app name and app id is correct.")
    mongodb_connector.add_or_update_data(reviews)
    return JSONResponse(status_code=200,
                        content={"message": "Reviews fetched successfully."})


@app.get("/get_reviews_metrics")
async def get_reviews_metrics(
        params: tuple = Depends(validate_and_process_params),
        mongodb_connector: MongoConnector = Depends(get_mongo_connector),
        metric_inference: MetricInference = Depends(get_metric_inference)):
    app_name, app_id = params

    reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)

    if not reviews or "reviews" not in reviews:
        raise HTTPException(status_code=404, detail="Reviews not found in the database.")

    reviews_list = reviews["reviews"]
    result = metric_inference.run(reviews_list)
    metrics = result["metrics"]
    improvement_suggestions = result["improvement_suggestions"]

    return JSONResponse(status_code=200,
                        content={"metrics": metrics,
                                 "improvement_suggestions": improvement_suggestions})


@app.get("/download_reviews")
async def download_reviews(
        params: tuple = Depends(validate_and_process_params),
        mongodb_connector: MongoConnector = Depends(get_mongo_connector)):
    app_name, app_id = params

    reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)
    if not reviews or "reviews" not in reviews:
        raise HTTPException(status_code=404, detail="Reviews not found in the database.")

    reviews_list = reviews["reviews"]
    file_path = f"reviews/{app_name}.json"
    try:
        with open(file_path, "w") as f:
            json.dump(reviews_list, f)
        
        return FileResponse(file_path, filename=f"{app_name}_reviews.json")

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
