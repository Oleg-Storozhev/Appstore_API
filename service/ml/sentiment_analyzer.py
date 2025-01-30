from textblob import TextBlob


class SentimentAnalyzer:
    @staticmethod
    def get_sentiment(text: str) -> str:
        """Returns the sentiment of a given text."""
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.1:
            return "Positive"
        if polarity < -0.1:
            return "Negative"
        return "Neutral"
