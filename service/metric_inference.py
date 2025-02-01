from service.ml.improvement_suggestions_summarizer import ImprovementSuggestionsSummarizer
from service.ml.keyword_extractor import KeywordExtractor
from service.ml.metrics_calculator import MetricsCalculator


class MetricInference:
    def __init__(self):
        self.improvement_suggestions_summarizer = ImprovementSuggestionsSummarizer()

    def get_metrics(self, reviews: list) -> dict:
        metrics = MetricsCalculator.get_metrics(reviews)
        return metrics

    def get_improvement_suggestions(self, reviews: list) -> str:
        negative_keywords = KeywordExtractor.extract_keywords_keybert(reviews)
        improvement_suggestions = self.improvement_suggestions_summarizer.generate_insight(negative_keywords)
        return improvement_suggestions

    def run(self, reviews: list) -> dict:
        metrics = self.get_metrics(reviews)
        improvement_suggestions = self.get_improvement_suggestions(reviews)
        return {"metrics": metrics,
                "improvement_suggestions": improvement_suggestions}
