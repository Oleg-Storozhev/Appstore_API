import pandas as pd


class MetricsCalculator:
    @staticmethod
    def get_metrics(processed_reviews: list):
        df = pd.DataFrame(processed_reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])
        mean_rating = df.rating.mean()
        ratings_distribution_count = df.rating.value_counts()
        ratings_distribution_percentage = df.rating.value_counts(normalize=True) * 100

        return {
            "mean_rating": mean_rating,
            "ratings_distribution": ratings_distribution_count.to_dict(),
            "ratings_distribution_percentage": ratings_distribution_percentage.to_dict()
        }