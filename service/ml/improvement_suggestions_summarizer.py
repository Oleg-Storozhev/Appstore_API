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
                                       repetition_penalty=1.25,
                                       return_full_text=False,
                                       huggingfacehub_api_token=HF_KEY)

        self.suggestion_prompt_text = """You are an AI expert in product reviews and user experience analysis.
        A list of key phrases has been extracted from negative reviews of an application in the App Store.
        Your task is to analyze these phrases, identify common issues, and suggest specific improvements to enhance the user experience.
        
        ## Rules:
        1. Group similar issues together into clear and distinct categories. Each category should represent a unique issue.
        2. Start your response with a **bullet-point list of all identified issues** (one line per issue). Make the list concise but meaningful.
        3. After the list, provide a **detailed explanation for each issue**, including:
           - A summary of the issue.
           - A recommendation on how to address it.
           - Examples (if applicable) to clarify the recommendation.
        4. End your response with a **one-paragraph summary** of the key takeaways and overall suggestions.
        5. Only include key issues that indicate a real problem; ignore phrases that do not provide actionable feedback.
        6. Do not introduce new issues, keywords, or suggestions that are not explicitly mentioned in the provided list.
        7. Write professionally, maintaining a natural and business-oriented tone. Avoid overly long sentences or unnecessary repetition.
        8. Each recommendation must start on a new line and be actionable.
        
        ## Template for Response:
        ### Detailed Analysis and Recommendations:
        #### Issue 1: [Short description]
        - **Details:** [Detailed explanation of the issue.]
        - **Recommendation:** [Clear and actionable solution.]
        
        #### Issue 2: [Short description]
        - **Details:** [Detailed explanation of the issue.]
        - **Recommendation:** [Clear and actionable solution.]
        
        ... [Repeat for other issues as necessary]
        
        ### Summary:
        [One-paragraph summary highlighting the main takeaways and overall suggestions.]
        
        ## Key Phrases:
        List of key phrases from negative reviews: {keywords}
        """

        self.suggestion_prompt = PromptTemplate(
            input_variables=["keywords"],
            template=self.suggestion_prompt_text
        )
        self.suggestion_chain = self.suggestion_prompt | self.llm

    def generate_insight(self, keywords):
        if not keywords:
            return "No major concerns identified."

        suggestion_result = self.suggestion_chain.invoke({"keywords": keywords})
        suggestion_result = re.sub(r"[^\S\r\n]+", " ", suggestion_result)
        suggestion_result = re.sub(r"\n+", "\n", suggestion_result)
        suggestion_result = suggestion_result.strip()
        return suggestion_result
