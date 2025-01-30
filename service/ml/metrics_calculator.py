import pandas as pd

from service.ml.keyword_extractor import KeywordExtractor


class MetricsCalculator:
    @staticmethod
    def get_metrics(processed_reviews: list):
        df = pd.DataFrame(processed_reviews, columns=["title", "rating", "review", "cleaned_text", "sentiment"])
        mean_rating = df.rating.mean()
        ratings_distribution_count = df.rating.value_counts()
        ratings_distribution_percentage = df.rating.value_counts(normalize=True) * 100
        negative_keywords = KeywordExtractor.extract_negative_keywords(processed_reviews)

        improvement_areas = "Focus on improving aspects related to these common complaints: " + ", ".join(negative_keywords) if negative_keywords else "No major concerns identified."

        return {
            "mean_rating": mean_rating,
            "ratings_distribution": ratings_distribution_count.to_dict(),
            "ratings_distribution_percentage": ratings_distribution_percentage.to_dict(),
            "common_negative_keywords": negative_keywords,
            "improvement_suggestions": improvement_areas
        }