import sys
import os
import re
# from streamlit_mermaid import st_mermaid
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
import streamlit.components.v1 as components

from orchestrator.workflow import WorkflowOrchestrator


def extract_mermaid(markdown_text):

    pattern = r"```mermaid\s*(.*?)```"

    matches = re.findall(
        pattern,
        markdown_text,
        re.DOTALL
    )

    cleaned_matches = []

    for match in matches:

        cleaned = (
            match
            .replace("\r", "")
            .strip()
        )

        cleaned_matches.append(cleaned)

    return cleaned_matches


# def render_mermaid(mermaid_code):
#
#     html = f"""
#     <!DOCTYPE html>
#     <html>
#
#     <head>
#
#       <script type="module">
#         import mermaid from
#         'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
#
#         window.addEventListener('load', async () => {{
#
#             mermaid.initialize({{
#                 startOnLoad: false
#             }});
#
#             const element =
#                 document.getElementById("mermaid-diagram");
#
#             try {{
#
#                 const {{ svg }} =
#                     await mermaid.render(
#                         "graphDiv",
#                         `{mermaid_code}`
#                     );
#
#                 element.innerHTML = svg;
#
#             }} catch (err) {{
#
#                 element.innerHTML =
#                     "<pre>" + err + "</pre>";
#
#                 console.error(err);
#             }}
#         }});
#       </script>
#
#     </head>
#
#     <body>
#
#         <div id="mermaid-diagram"></div>
#
#     </body>
#
#     </html>
#     """
#
#     components.html(
#         html,
#         height=600,
#         scrolling=True
#     )
from graphviz import Digraph


def build_sequence_diagram(text):

    dot = Digraph()

    dot.attr(rankdir="LR")

    participants = set()

    lines = text.splitlines()

    interactions = []

    pattern = r"(\w+)\s*->\s*(\w+)\s*:\s*(\w+)"

    for line in lines:

        line = line.strip()

        match = re.search(pattern, line)

        if not match:
            continue

        source = match.group(1)
        target = match.group(2)
        command = match.group(3)

        participants.add(source)
        participants.add(target)

        interactions.append(
            (source, target, command)
        )

    # Create Nodes
    for participant in participants:

        dot.node(
            participant,
            shape="box",
            style="filled",
            fillcolor="lightblue"
        )

    # Create Edges
    for source, target, command in interactions:

        dot.edge(
            source,
            target,
            label=command
        )

    return dot


st.set_page_config(
    page_title="AI TANGO Engineering System",
    layout="wide"
)

st.title("AI Multi-Agent TANGO Engineering System")

st.markdown(
    "AI-assisted TANGO feature development using multi-agent workflow."
)

user_requirement = st.text_area(
    "Enter Feature Requirement",
    height=200,
    placeholder="""
Example:

Implement TelescopeON command orchestration.

Requirements:
- MonitoringDevice invokes TelescopeON on Device2 and Device3
- Wait for ResultCode.OK from all devices
- Return FAILED if any device fails
"""
)

if st.button("Generate"):

    orchestrator = WorkflowOrchestrator()

    with st.spinner("AI Agents Processing..."):

        result = orchestrator.run(user_requirement)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Requirements",
        "Architecture",
        "Mermaid Diagram",
        "Generated Devices"
    ])

    # =====================================================
    # Requirements Tab
    # =====================================================

    with tab1:

        st.json(result["requirement_output"])

    # =====================================================
    # Architecture Tab
    # =====================================================

    with tab2:

        st.markdown(result["architecture_output"])

    # =====================================================
    # Mermaid Diagram Tab
    # =====================================================

    # with tab3:
    #
    #     mermaid_blocks = extract_mermaid(
    #         result["architecture_output"]
    #     )
    #
    #     if not mermaid_blocks:
    #
    #         st.error("No Mermaid diagram found")
    #
    #     else:
    #
    #         for block in mermaid_blocks:
    #
    #             cleaned = block.strip()
    #
    #             st.code(cleaned, language="text")
    #
    #             render_mermaid(cleaned)
    with tab3:

        st.subheader(
            "AI Generated Sequence Diagram"
        )

        diagram = build_sequence_diagram(
            result["architecture_output"]
        )

        st.graphviz_chart(diagram)

    # =====================================================
    # Generated Devices Tab
    # =====================================================

    with tab4:

        st.markdown(result["device_output"])

    # =====================================================
    # Generated Files
    # =====================================================

    st.subheader("Generated Files")

    for root, dirs, files in os.walk(
        "outputs/generated_project"
    ):

        for file in files:

            st.text(
                os.path.join(root, file)
            )