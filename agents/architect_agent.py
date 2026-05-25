from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class ArchitectAgent:

    def design(self, requirements: dict):

        prompt = f"""
        You are a senior distributed systems architect specialized in TANGO Controls telescope systems.
        
        Using the following structured requirements, generate:
        
        1. TANGO device hierarchy
        2. Device responsibilities
        3. Backend architecture
        4. Communication model
        5. REST APIs
        6. Deployment considerations
        7. Interaction flow for orchestration visualization
        
        Requirements:
        {requirements}
        
        IMPORTANT INTERACTION RULES:
        - Generate ONLY high-level inter-device communication flow
        - Focus ONLY on orchestration interactions
        - Include:
          - command invocation
          - downstream command propagation
          - result propagation
          - final aggregated response
        - Do NOT include:
          - logging internals
          - retries
          - timeout checker methods
          - helper methods
          - threading internals
          - status polling loops
          - self interactions
          - internal implementation details
        - Never generate SOURCE -> SAME_SOURCE interactions
        - Keep orchestration minimal and readable
        
        IMPORTANT FLOW FORMAT:
        Generate interaction flow using EXACT syntax below:
        
        Client -> CentralNode : TelescopeON
        CentralNode -> CSPMaster : TelescopeON
        CentralNode -> SDPMaster : TelescopeON
        CSPMaster -> CentralNode : RESULT_OK
        SDPMaster -> CentralNode : RESULT_OK
        CentralNode -> Client : RESULT_OK
        
        IMPORTANT:
        - Use only one interaction per line
        - Do not use markdown tables for interactions
        - Do not use bullets for interactions
        - Use only:
          SOURCE -> TARGET : COMMAND
        - Keep command names short
        - Keep device names concise
        - Avoid duplicate interactions
        
        Return response in markdown format.
        """

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert TANGO Controls architect "
                        "specialized in distributed orchestration systems."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return response.choices[0].message.content