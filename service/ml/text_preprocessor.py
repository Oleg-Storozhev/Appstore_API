import re
import emoji


class TextPreprocessor:
    @staticmethod
    def clean_text(text: str) -> str:
        text = emoji.replace_emoji(text, replace='')  # Remove emojis
        text = text.replace("\n", " ")  # Remove new lines
        text = text.replace("!.", "! ")
        text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
        return text
