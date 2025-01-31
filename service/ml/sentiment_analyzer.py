from textblob import TextBlob


class SentimentAnalyzer:
    @staticmethod
    def get_sentiment(text: str) -> str:
        """Returns the sentiment of a given text."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.05:
            return "Positive"
        if polarity < -0.05:
            return "Negative"
        return "Neutral"
