from sklearn.feature_extraction.text import TfidfVectorizer


class KeywordExtractor:
    @staticmethod
    def extract_negative_keywords(reviews):
        """Identifies common keywords in negative reviews using TF-IDF."""
        negative_reviews = [review['cleaned_text'] for review in reviews if review['sentiment'] == "Negative"]
        if not negative_reviews:
            return []

        vectorizer = TfidfVectorizer(stop_words='english', max_features=10, ngram_range=(2, 3))
        X = vectorizer.fit_transform(negative_reviews)
        keywords = vectorizer.get_feature_names_out()
        return list(keywords)
