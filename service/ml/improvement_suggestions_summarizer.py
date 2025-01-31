import re

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from service.core.local_enviroments import HF_KEY


class ImprovementSuggestionsSummarizer:
    def __init__(self):
        self.llm = HuggingFaceEndpoint(model="mistralai/Mistral-7B-Instruct-v0.1",
                                       task="text-generation",
                                       max_new_tokens=256,
                                       temperature=0.1,
                                       return_full_text=False,
                                       huggingfacehub_api_token=HF_KEY)

        self.suggestion_prompt_text = """You are an expert in product reviews and user experience analysis.
        From the negative reviews the keywords and key phrases were extracted for the application in AppStore.
        Your task is to look at the list of keywords/phrases and suggest improvement for the application.
        
        ### Rules:
        1) Merge similar suggestions together to avoid redundancy.
        2) Filter the suggestions, keep only the most important ones.
        3) Write an answer in a concise manner. 
        4) Keep it clear and user-friendly, but business intelligence.
        5) Make a summarization of the suggestions.
        6) Don't make up new ideas.
        7) Don't make up new keywords.
        8) Don't make up new phrases.
        9) Don't write a long answer.
        10) Don't use headers in answer.
        11) Don't use bold text in answer.
        12) Don't use italics in answer.
        13) Don't use bullet points in answer.
            
        List of the keywords from negative reviews: {keywords}
        """

        self.suggestion_prompt = PromptTemplate(
            input_variables=["keywords"],
            template=self.suggestion_prompt_text
        )
        self.suggestion_chain = self.suggestion_prompt | self.llm

    def generate_insight(self, keywords):
        """Generates insights using GPT-3.5 Turbo based on extracted keywords."""
        if not keywords:
            return "No major concerns identified."

        # prompt = self.suggestion_prompt.format(keywords=", ".join(keywords))
        suggestion_result = self.suggestion_chain.invoke({"keywords": keywords})
        suggestion_result = re.sub(r"\n+", "\n", suggestion_result)
        suggestion_result = re.sub(r"\s+", " ", suggestion_result)
        suggestion_result = suggestion_result.strip("\n")
        suggestion_result = suggestion_result.strip()
        print(suggestion_result)
        return suggestion_result
