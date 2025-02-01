import pandas as pd


class MetricsCalculator:
    @staticmethod
    def create_df(reviews: list) -> pd.DataFrame:
        return pd.DataFrame(reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])

    @staticmethod
    def calculate_for_rating(df: pd.DataFrame):
        mean_rating = df.rating.mean()
        ratings_distribution_count = df.rating.value_counts().to_dict()
        return mean_rating, ratings_distribution_count

    @staticmethod
    def calculate_for_sentiment(df: pd.DataFrame):
        sentiment_distribution_count = df.sentiment.value_counts().to_dict()
        return sentiment_distribution_count

    @staticmethod
    def get_metrics(reviews: list):
        df = MetricsCalculator.create_df(reviews)
        mean_rating, ratings_count = MetricsCalculator.calculate_for_rating(df)
        sentiment_count = MetricsCalculator.calculate_for_sentiment(df)

        return {
            "mean_rating": mean_rating,
            "ratings_distribution_count": ratings_count,
            "sentiment_distribution_count": sentiment_count,
        }
