from keybert import KeyBERT


class KeywordExtractor:
    @staticmethod
    def extract_keywords_keybert(reviews):
        negative_reviews = " ".join([review['cleaned_text'] for review in reviews if review['sentiment'] == "Negative"])
        if not negative_reviews:
            return []

        kw_model = KeyBERT()
        keywords = kw_model.extract_keywords(negative_reviews, keyphrase_ngram_range=(2, 7), use_mmr=True, diversity=0.35, top_n=30)
        return [kw[0] for kw in keywords]
