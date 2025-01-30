import uvicorn
import json
import re
import emoji

import pandas as pd

from textblob import TextBlob
from app_store_scraper import AppStore
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse

from sklearn.feature_extraction.text import CountVectorizer

app = FastAPI()


def extract_negative_keywords(reviews):
    """Identifies common keywords in negative reviews."""
    negative_reviews = [review['cleaned_text'] for review in reviews if review['sentiment'] == "Negative"]
    if not negative_reviews:
        return []

    vectorizer = CountVectorizer(stop_words='english', max_features=10, ngram_range=(2, 5))
    X = vectorizer.fit_transform(negative_reviews)
    keywords = vectorizer.get_feature_names_out()
    return list(keywords)


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


def get_metrics(processed_reviews: list):
    df = pd.DataFrame(processed_reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])
    mean_rating = df.rating.mean()
    ratings_distribution_count = df.rating.value_counts()
    ratings_distribution_percentage = df.rating.value_counts(normalize=True) * 100
    negative_keywords = extract_negative_keywords(processed_reviews)

    improvement_areas = "Focus on improving aspects related to these common complaints: " + ", ".join(negative_keywords) if negative_keywords else "No major concerns identified."

    return {
        "mean_rating": mean_rating,
        "ratings_distribution": ratings_distribution_count.to_dict(),
        "ratings_distribution_percentage": ratings_distribution_percentage.to_dict(),
        "common_negative_keywords": negative_keywords,
        "improvement_suggestions": improvement_areas
    }


@app.get("/healthcheck")
async def test():
    return JSONResponse(content={"message": "API is running!"})


@app.get("/get_reviews")
async def get_reviews(app_name: str, app_id: str):
    reviews = fetch_reviews(app_name=app_name, app_id=app_id)
    metrics = get_metrics(reviews)
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
