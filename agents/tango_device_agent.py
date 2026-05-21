from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class TangoDeviceAgent:

    def generate(
        self,
        requirement_output: dict,
        workflow_output: str
    ):

        prompt = f"""
You are a senior TANGO Controls engineer.

Your task is to generate production-quality TANGO device orchestration code.

SYSTEM CONTEXT:
- This is a distributed telescope control system
- Devices communicate using TANGO DeviceProxy
- Commands may involve orchestration across multiple devices
- Reliability and fault handling are important

REQUIREMENTS:
{requirement_output}

WORKFLOW DESIGN:
{workflow_output}

IMPLEMENTATION REQUIREMENTS:

1. Generate Python TANGO device classes
2. Use PyTango style APIs
3. Include:
   - commands
   - attributes
   - ResultCode handling
   - timeout handling
   - logging
   - exception handling
   - state transitions
4. Generate realistic orchestration logic
5. Add comments explaining important sections
6. Use DeviceProxy where required
7. Assume asynchronous orchestration where appropriate

IMPORTANT:
- Generate production-style engineering code
- Do not generate toy examples
- Focus on orchestration and distributed command handling
- Consider partial failure handling
- Consider device communication failure

RETURN FORMAT:

FILE: devices/monitoring_device.py

<python code>

FILE: devices/device2.py

<python code>

FILE: devices/device3.py

<python code>

FEATURE TO IMPLEMENT:
The MonitoringDevice receives TelescopeON command.
It invokes TelescopeON on Device2 and Device3.
It waits for ResultCode.OK from all devices.
If all devices succeed:
    return ResultCode.OK
Else:
    return ResultCode.FAILED
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert distributed systems "
                        "and TANGO Controls engineer."
                    )
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.1
        )

        return response.choices[0].message.content