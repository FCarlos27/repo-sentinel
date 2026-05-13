import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class GroqAgent:
    def __init__(self):
        """
        GroqAI Client Object 
        """
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found. Check your .env file.")
        
        self.client = Groq(api_key=api_key)
        self.model_id = "llama-3.3-70b-versatile"

    def analyze_code(self, code_snippet: str):
        try:
            completion = self.client.chat.completions.create(
                model=self.model_id,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a Senior Systems Engineer auditing code for security leaks and technical debt."
                    },
                    {
                        "role": "user", 
                        "content": f"Audit this code snippet:\n\n{code_snippet}"
                    }
                ],
                temperature=0.5,
            )
            return completion.choices[0].message.content
        except Exception as e:
            return f"Groq Analysis Error: {str(e)}"

