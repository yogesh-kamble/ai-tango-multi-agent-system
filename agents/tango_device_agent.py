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

        Your task is to generate production-quality executable TANGO device orchestration code.

        SYSTEM CONTEXT:
        - This is a distributed telescope control system
        - Devices communicate using TANGO DeviceProxy
        - Commands may involve orchestration across multiple devices
        - Reliability, observability, and fault handling are important
        - Generated code must run directly in standard PyTango environments

        REQUIREMENTS:
        {requirement_output}

        WORKFLOW DESIGN:
        {workflow_output}

        IMPLEMENTATION REQUIREMENTS:

        1. Generate Python TANGO device classes
        2. Use standard stable PyTango APIs
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
        8. Generate executable code compatible with standard PyTango runtime
        9. Prefer compatibility and runtime stability over framework verbosity
        10. Configure Tango change events correctly for event-driven attributes
        11. Ensure all event attributes are properly initialized during device startup
        12. Generate fully operational TANGO event handling code
        13. configure logging level to info

        IMPORTANT IMPLEMENTATION RULES:
        - Implement orchestration exactly as defined in workflow design
        - Generate only the devices required by architecture
        - Use DeviceProxy for downstream device communication
        - Implement realistic distributed command execution
        - Handle downstream failures gracefully
        - Implement aggregated ResultCode handling where orchestration exists
        - Generate production-style engineering code
        - Do not generate toy examples
        - Do not hardcode telescope commands unless present in requirements
        - Generate code that runs directly without manual fixes
        - Avoid unsupported or version-specific Tango APIs
        - Prefer minimal stable APIs over verbose attribute configuration
        - Avoid unnecessary Tango metadata configuration
        - Ensure all imports are valid
        - Ensure device server startup works correctly
        - Ensure commands execute without syntax/runtime errors
        - Generate code comptabilble with pytango 10.1.4 and above
        
        COMMAND DECORATOR RULES:
        - Always use:
            @command(dtype_out=...)
          for command return values
        - Never use:
            @command(dtype=...)
        - For commands without input:
            @command(dtype_out=int)
        - For commands with input:
            @command(dtype_in=str, dtype_out=int)
        - Generate runtime-compatible Tango command decorators only
        
        Do not use Tango event subscriptions or push_change_event.
        Use simple synchronous attribute reads for status tracking.
        Focus on orchestration logic and distributed command handling.
        Generate stable executable code suitable for demo purposes.

        IMPORTANT PYTANGO COMPATIBILITY RULES:
        - Use:
            attribute(dtype=str, access=AttrWriteType.READ)
          instead of verbose optional attribute metadata
        - Avoid:
            label=
            description=
            display_level=
            data_format=
            data_type=
          unless explicitly required
        - Use:
            run((DeviceClass,))
          instead of:
            run((DeviceClass,), "DeviceClass")
        - Prefer simple stable attribute definitions
        - Generate runtime-compatible code for common PyTango installations
        - Use import tango and tango.server APIs only.
        - Do not use PyTango imports.
        - Use run((DeviceClass,)) for server startup.
        - DeviceProxy does not provide get_name().
        - Use dev_name() or maintain the device name separately.
        - Generate code compatible with PyTango 10.x.
        - Do not invent Tango APIs or methods.
        
        API VALIDATION RULES:

        - Use only documented PyTango APIs.
        - Do not invent helper methods.
        - Do not use:
            tango.get_clock()
            tango.Timer()
            DeviceProxy.get_name()
            PyTango.command()
            PyTango.server_run()

        - If a timer is needed, use Python time module.
        - All imports must be explicitly included.
        - Generated code must be syntactically executable without modification.
        
        ASYNC ORCHESTRATION RULES

        * Any command involving downstream devices must execute asynchronously.
        * Command handlers must return ResultCode.QUEUED immediately.
        * Never wait for downstream completion inside a Tango command method.
        * Use a single background orchestration thread.
        * The orchestration thread shall:
        
          * invoke downstream commands
          * monitor CommandStatus attributes
          * handle timeouts and exceptions
          * aggregate results
          * update local CommandStatus
        * CommandStatus lifecycle:
          QUEUED -> RUNNING -> OK/FAILED
        * All downstream operations must have explicit timeout handling.
        * Clients should monitor CommandStatus instead of waiting for command completion.

        
        TANGO THREADING RULES:
        - Background threads interacting with Tango APIs must use:
            with tango.EnsureOmniThread():
        - Any thread calling:
            push_change_event
            set_state
            DeviceProxy
            Tango APIs
          must use EnsureOmniThread
        - Tango device APIs are not automatically thread-safe
        - Avoid direct Tango API access from unmanaged threads
        - Protect shared state with threading.Lock
        - Avoid Tango monitor deadlocks
        - Event pushing from worker threads must use EnsureOmniThread
        
        THREADING RULES:
        - Use instance-level locks only.
        - Never declare threading.Lock() as a class variable.
        - Never acquire a lock and call another method that acquires the same lock.
        - Use threading.RLock only when recursive locking is required.
        - Keep worker threads independent from Tango APIs.
        - Worker threads should only update internal Python state.
    
        IMPORT AND FRAMEWORK RULES:
        - Use modern tango package APIs
        - Do NOT use deprecated PyTango APIs
        - Always use:
        
            from tango.server import Device, attribute, command, run
            from tango import DeviceProxy, DevState, AttrWriteType
    
        - Never use:
            PyTango.server_run
            DeviceMeta
            PyTango.command
            from PyTango import ResultCode
        
        EXPECTED IMPORT STYLE:

        import threading
        import logging
        from enum import Enum
        
        import tango
        from tango import DevState, AttrWriteType, DeviceProxy
        from tango.server import Device, attribute, command, run

        - ResultCode must always be custom Enum generated in code
        - Generate runtime-compatible imports only
        - Use stable modern PyTango/Tango syntax
        
        EXPECTED IMPORT STYLE:

        import threading
        import logging
        from enum import Enum
        
        import tango
        from tango import DevState, AttrWriteType, DeviceProxy
        from tango.server import Device, attribute, command, run

        CODE QUALITY RULES:
        - Use proper threading where async orchestration is needed
        - Use locks for shared state updates
        - Use structured logging
        - Add clear comments for orchestration logic
        - Handle exceptions explicitly
        - Handle timeout scenarios cleanly
        - Avoid pseudo-code
        - Avoid incomplete implementations
        - Return realistic ResultCode values

        RETURN FORMAT:

        FILE: devices/<device_name>.py

        <python code>
        """

        response = client.chat.completions.create(
            model="gpt-4.1",
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