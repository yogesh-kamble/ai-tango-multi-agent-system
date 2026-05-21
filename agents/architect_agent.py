from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class ArchitectAgent:

    def design(self, requirements: dict):
        prompt = f"""
        You are a senior distributed systems architect specialized in TANGO Controls telescope systems.

        Using the following structured requirements, generate:

        1. TANGO device hierarchy
        2. Device responsibilities
        3. Backend architecture
        4. Communication model
        5. Deployment considerations
        6. Mermaid architecture diagram

        Requirements:
        {requirements}

        IMPORTANT Interaction Flow Rules:
        - Generate interaction flow using the exact syntax:
          SOURCE -> TARGET : COMMAND
        - Keep one interaction per line
        - Keep command names short
        - Use uppercase command names
        - Do not generate Mermaid syntax
        - Do not generate markdown tables
        - Interaction flow must represent orchestration sequence clearly


        Return response in markdown format.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert TANGO Controls architect."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3
        )

        return response.choices[0].message.content