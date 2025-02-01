from textblob import TextBlob


class SentimentAnalyzer:
    @staticmethod
    def get_sentiment(text: str) -> str:
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        if polarity > 0.05:
            return "Positive"
        if polarity < -0.05:
            return "Negative"
        return "Neutral"
