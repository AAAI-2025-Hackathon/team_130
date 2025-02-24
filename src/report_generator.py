from groq import Groq
from config import GROQ_API_KEY, MODEL_NAME
from src.prompts import REPORT_GENERATOR_SYSTEM_PROMPT, get_report_prompt

class ReportGenerator:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        
    def generate_report(self, interpretation):
        prompt = get_report_prompt(interpretation)
        
        completion = self.client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": REPORT_GENERATOR_SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1024
        )
        
        return completion.choices[0].message.content 