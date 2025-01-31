import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

from service.core.local_enviroments import API_KEY

os.environ["OPENAI_API_KEY"] = API_KEY


class ImprovementSuggestionsSummarizer:
    def __init__(self):
        self.suggestion_prompt_text = """
            You are an expert in product reviews and user experience analysis. 
            From the negative reviews the keywords and key phrases were extracted.
            Your task is look at the list of keywords and key phrases and suggest improvement suggestions.
            """

        self.suggestion_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", self.suggestion_prompt_text),
                ("user", "{input}"),
            ]
        )

        self.suggestion_chain = self.suggestion_prompt | ChatOpenAI(temperature=0.2, model_name="gpt-3.5-turbo")

    def generate_insight(self, keywords):
        """Generates insights using GPT-3.5 Turbo based on extracted keywords."""
        inputs = {"input": keywords}
        if not keywords:
            return "No major concerns identified."

        suggestion_result = self.suggestion_chain.invoke(inputs)

        return suggestion_result.content
