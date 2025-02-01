from app_store_scraper import AppStore

from service.ml.text_preprocessor import TextPreprocessor
from service.ml.sentiment_analyzer import SentimentAnalyzer


class ReviewFetcher:
    @staticmethod
    def fetch_reviews(app_name: str, app_id: str, country: str = "us", num_reviews: int = 100) -> dict:
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
                review["cleaned_text"] = TextPreprocessor.clean_text(title_and_review)
                review["sentiment"] = SentimentAnalyzer.get_sentiment(review["cleaned_text"])

            review_dict = {"app_id": app_id, "app_name": app_name, "reviews": processed_reviews}
            return review_dict

        except Exception as e:
            return {"error": str(e)}
