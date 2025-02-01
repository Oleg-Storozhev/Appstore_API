import json
import uvicorn

from pydantic import ValidationError

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, FileResponse

from service.connectors.mongodb_connector import MongoConnector
from service.metric_inference import MetricInference
from service.ml.review_fetcher import ReviewFetcher

app = FastAPI()
mongodb_connector = MongoConnector()
metric_inference = MetricInference()


@app.exception_handler(Exception)
async def global_exception_handler(request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request, exc: ValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )


@app.get("/healthcheck")
async def test():
    return JSONResponse(status_code=200,
                        content={"message": "API is running!"})


@app.post("/get_reviews")
async def get_reviews(app_name: str, app_id: str):
    try:
        reviews = ReviewFetcher.fetch_reviews(app_name=app_name, app_id=app_id)
        mongodb_connector.add_or_update_data(reviews)
        return JSONResponse(status_code=200,
                            content={"message": "Reviews fetched successfully."})
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to fetch and store reviews.")


@app.get("/get_reviews_metrics")
async def get_reviews_metrics(app_name: str, app_id: str):
    try:
        reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)
        if not reviews or "reviews" not in reviews:
            raise HTTPException(status_code=404, detail="Reviews not found in the database.")
        reviews_list = reviews["reviews"]
        result = metric_inference.run(reviews_list)
        metrics = result["metrics"]
        improvement_suggestions = result["improvement_suggestions"]

        return JSONResponse(status_code=200,
                            content={"metrics": metrics,
                                     "improvement_suggestions": improvement_suggestions
                                     })
    except KeyError:
        raise HTTPException(status_code=404, detail="Reviews data is improperly structured or missing.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to compute review metrics.")


@app.get("/download_reviews")
async def download_reviews(app_name: str, app_id: str):
    try:
        reviews = mongodb_connector.get_data(app_name=app_name, app_id=app_id)
        if not reviews or "reviews" not in reviews:
            raise HTTPException(status_code=404, detail="Reviews not found in the database.")
        reviews_list = reviews["reviews"]
        file_path = f"reviews/{app_name}.json"
        with open(file_path, "w") as f:
            json.dump(reviews_list, f)

        return FileResponse(file_path, filename=f"{app_name}_reviews.json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found.")
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to prepare the download.")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
