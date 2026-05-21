from agents.requirement_agent import RequirementAgent
from agents.architect_agent import ArchitectAgent
from agents.tango_device_agent import TangoDeviceAgent
from utils.file_parser import (
    extract_files,
    save_generated_files
)

import json
import os


class WorkflowOrchestrator:

    def __init__(self):

        self.requirement_agent = RequirementAgent()
        self.architect_agent = ArchitectAgent()
        self.tango_device_agent = TangoDeviceAgent()

        os.makedirs("outputs", exist_ok=True)

    def run(self, user_input: str):
        requirement_output = self.requirement_agent.analyze(
            user_input
        )

        architecture_output = self.architect_agent.design(
            requirement_output
        )

        device_output = self.tango_device_agent.generate(
            requirement_output, architecture_output
        )

        # Save requirements
        with open(
                "outputs/requirements.json",
                "w"
        ) as f:
            json.dump(
                requirement_output,
                f,
                indent=2,
                default=str
            )

        # Save architecture
        with open(
                "outputs/architecture.md",
                "w"
        ) as f:
            f.write(architecture_output)

        # Save device output
        with open(
                "outputs/device_generation.md",
                "w"
        ) as f:
            f.write(device_output)

        generated_files = extract_files(device_output)

        save_generated_files(generated_files)

        return {
            "requirement_output": requirement_output,
            "architecture_output": architecture_output,
            "device_output": device_output
        }