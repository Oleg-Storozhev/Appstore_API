import uvicorn
import json
import re
import emoji

from textblob import TextBlob
from app_store_scraper import AppStore
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()


def get_sentiment(text: str) -> str:
    """Returns the sentiment of a given text."""
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.1:
        return "Positive"
    if polarity < -0.1:
        return "Negative"
    return "Neutral"


def clean_text(text: str) -> str:
    """Preprocesses text by removing special characters and extra spaces."""
    text = emoji.replace_emoji(text, replace='')  # Remove emojis
    text = text.replace("\n", " ")  # Remove new lines
    text = text.replace("!.", "! ")
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text


def fetch_reviews(app_name: str, app_id: str, country: str = "us", num_reviews: int = 100):
    try:
        app = AppStore(country=country, app_name=app_name, app_id=app_id)
        app.review(how_many=num_reviews)
        reviews = app.reviews
        if not reviews:
            return {"error": "No reviews found."}

        processed_reviews = []
        for review in reviews:
            processed_reviews.append({
                "title": review.get("title", ""),
                "rating": review.get("rating", "No rating"),
                "review": review.get("review", "")
            })

        for review in processed_reviews:
            title_and_review = review["title"] + ". " + review["review"]
            review["cleaned_text"] = clean_text(title_and_review)
            review["sentiment"] = get_sentiment(review["cleaned_text"])
        return processed_reviews

    except Exception as e:
        return {"error": str(e)}


@app.get("/healthcheck")
async def test():
    return JSONResponse(content={"message": "API is running!"})


@app.get("/get_reviews")
async def get_reviews(app_name: str, app_id: str):
    reviews = fetch_reviews(app_name=app_name, app_id=app_id)
    metrics = {}
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
