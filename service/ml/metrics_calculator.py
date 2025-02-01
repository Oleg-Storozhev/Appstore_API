import pandas as pd


class MetricsCalculator:
    @staticmethod
    def create_df(reviews: list) -> pd.DataFrame:
        return pd.DataFrame(reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])

    @staticmethod
    def calculate_for_rating(df: pd.DataFrame):
        mean_rating = df.rating.mean()
        median_rating = df.rating.median()
        ratings_variation = df.rating.std()

        ratings_distribution_count = df.rating.value_counts().to_dict()
        ratings_count_percentage = df.rating.value_counts(normalize=True).to_dict()
        mode_rating = max(ratings_distribution_count, key=ratings_distribution_count.get)

        return {
            "mean_rating": mean_rating,
            "median_rating": median_rating,
            "mode_rating": mode_rating,
            "ratings_variation": ratings_variation,
            "ratings_count_percentage": ratings_count_percentage,
            "ratings_distribution_count": ratings_distribution_count,
        }

    @staticmethod
    def calculate_for_sentiment(df: pd.DataFrame):
        sentiment_distribution_count = df.sentiment.value_counts().to_dict()
        sentiment_count_percentage = df.sentiment.value_counts(normalize=True).to_dict()
        sentiment_mode = max(sentiment_distribution_count, key=sentiment_distribution_count.get)
        return {
            "sentiment_distribution_count": sentiment_distribution_count,
            "sentiment_count_percentage": sentiment_count_percentage,
            "sentiment_mode": sentiment_mode,
        }

    @staticmethod
    def get_metrics(reviews: list):
        df = MetricsCalculator.create_df(reviews)
        rating_metrics = MetricsCalculator.calculate_for_rating(df)
        sentiment_metrics = MetricsCalculator.calculate_for_sentiment(df)

        return {
            **rating_metrics,
            **sentiment_metrics
        }
