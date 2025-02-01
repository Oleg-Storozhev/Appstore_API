import pandas as pd


class MetricsCalculator:
    @staticmethod
    def create_df(reviews: list) -> pd.DataFrame:
        return pd.DataFrame(reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])

    @staticmethod
    def calculate_for_rating(df: pd.DataFrame):
        mean_rating = df.rating.mean()
        ratings_distribution_count = df.rating.value_counts()
        ratings_distribution_percentage = df.rating.value_counts(normalize=True) * 100
        return ratings_distribution_count.to_dict(), ratings_distribution_percentage.to_dict(), mean_rating,

    @staticmethod
    def calculate_for_sentiment(df: pd.DataFrame):
        sentiment_distribution_count = df.sentiment.value_count()
        sentiment_distribution_percentage = df.sentiment.value_counts(normalize=True) * 100
        return sentiment_distribution_count.to_dict(), sentiment_distribution_percentage.to_dict()

    @staticmethod
    def get_metrics(reviews: list):
        df = MetricsCalculator.create_df(reviews)
        ratings_count, ratings_percentage, mean_rating = MetricsCalculator.calculate_for_rating(df)
        sentiment_count, sentiment_percentage = MetricsCalculator.calculate_for_sentiment(df)

        return {
            "ratings_distribution_count": ratings_count,
            "ratings_distribution_percentage": ratings_percentage,
            "mean_rating": mean_rating,
            "sentiment_distribution_count": sentiment_count,
            "sentiment_distribution_percentage": sentiment_percentage
        }
