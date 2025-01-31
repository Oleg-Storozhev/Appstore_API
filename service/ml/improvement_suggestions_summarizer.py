from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import PromptTemplate

from service.core.local_enviroments import HF_KEY


class ImprovementSuggestionsSummarizer:
    def __init__(self):
        self.llm = HuggingFaceEndpoint(model="mistralai/Mistral-7B-Instruct-v0.1",
                                       task="text-generation",
                                       max_new_tokens=200,
                                       temperature=0.2,
                                       return_full_text=False,
                                       huggingfacehub_api_token=HF_KEY)
        self.suggestion_prompt_text = """
            You are an expert in product reviews and user experience analysis. 
            From the negative reviews the keywords and key phrases were extracted.
            Your task is to look at the list of keywords and key phrases and suggest improvement suggestions.
            Write the suggestions in a concise and concise manner.
            Write them in one paragraph.
            
            List of the keywords from negative reviews: {keywords}
            """
        self.suggestion_prompt = PromptTemplate(
            input_variables=["keywords"],
            template=self.suggestion_prompt_text
        )

    def generate_insight(self, keywords):
        """Generates insights using GPT-3.5 Turbo based on extracted keywords."""
        if not keywords:
            return "No major concerns identified."

        prompt = self.suggestion_prompt.format(keywords=", ".join(keywords))
        suggestion_result = self.llm.invoke(prompt)
        print(suggestion_result)
        return suggestion_result
