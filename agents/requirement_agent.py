from openai import OpenAI
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class RequirementAgent:

    def analyze(self, user_requirement: str):

        prompt = f"""
You are a scientific telescope software requirement analyst.

Convert the following user requirement into structured JSON.

Requirement:
{user_requirement}

Return ONLY valid JSON.

Expected format:
{{
    "project_name": "",
    "domain": "",
    "devices": [],
    "features": [],
    "interfaces": []
}}
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert telescope software architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Remove markdown code block wrappers
        if content.startswith("```json"):
            content = content.replace("```json", "", 1)

        if content.startswith("```"):
            content = content.replace("```", "", 1)

        if content.endswith("```"):
            content = content[:-3]

        content = content.strip()

        try:
            return json.loads(content)

        except Exception as e:
            return {
                "error": "Invalid JSON generated",
                "exception": str(e),
                "raw_output": content
            }
