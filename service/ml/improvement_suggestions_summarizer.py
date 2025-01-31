import re

from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from service.core.local_enviroments import HF_KEY


class ImprovementSuggestionsSummarizer:
    def __init__(self):
        self.llm = HuggingFaceEndpoint(model="mistralai/Mistral-Small-24B-Base-2501",
                                       task="text-generation",
                                       max_new_tokens=512,
                                       temperature=0.1,
                                       return_full_text=False,
                                       huggingfacehub_api_token=HF_KEY)

        self.suggestion_prompt_text = """You are an AI expert in product reviews and user experience analysis.
        A list of key phrases has been extracted from negative reviews of an application in the App Store.
        Your task is to analyze these phrases, identify common issues, and suggest specific improvements to enhance the user experience.
        
        ## Rules:
        1.	Group similar issues together.
        2.	Only include key issues that indicate a real problem; ignore phrases that do not provide actionable feedback.
        3.	Provide clear and concise recommendations based on the identified problems.
        4.	Summarize the issues and solutions effectively, keeping the response professional and actionable.
        5.	Do not introduce new issues, keywords, or suggestions that are not explicitly mentioned in the provided list.
        6.	Maintain a natural, business-oriented writing style 
        7.	Each recommendation must start on a new line.
        
        List of key phrases from negative reviews: {keywords}
        """

        self.suggestion_prompt = PromptTemplate(
            input_variables=["keywords"],
            template=self.suggestion_prompt_text
        )
        self.suggestion_chain = self.suggestion_prompt | self.llm

    def generate_insight(self, keywords):
        """Generates insights using Mistral Small based on extracted keywords."""
        if not keywords:
            return "No major concerns identified."

        suggestion_result = self.suggestion_chain.invoke({"keywords": keywords})
        suggestion_result = re.sub(r"[^\S\r\n]+", " ", suggestion_result)
        suggestion_result = re.sub(r"\n+", "\n", suggestion_result)
        suggestion_result = suggestion_result.strip()
        print(suggestion_result)
        return suggestion_result
