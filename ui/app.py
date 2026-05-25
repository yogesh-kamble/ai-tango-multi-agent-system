import sys
import os
import re
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import streamlit as st
from graphviz import Digraph

from orchestrator.workflow import WorkflowOrchestrator


# =========================================================
# Build UML Style Sequence Diagram
# =========================================================

def build_sequence_diagram(text):

    dot = Digraph("SequenceDiagram")

    dot.attr(
        rankdir="LR",
        splines="polyline",
        nodesep="1.0",
        ranksep="1.5",
        bgcolor="white"
    )

    participants = []
    interactions = []

    pattern = r"(\w+)\s*->\s*(\w+)\s*:\s*(\w+)"

    lines = text.splitlines()

    for line in lines:

        line = line.strip()

        match = re.search(pattern, line)

        if not match:
            continue

        source = match.group(1)
        target = match.group(2)
        command = match.group(3)

        if source not in participants:
            participants.append(source)

        if target not in participants:
            participants.append(target)

        interactions.append(
            (source, target, command)
        )

    # =====================================================
    # Create Participant Nodes
    # =====================================================

    for participant in participants:

        dot.node(
            participant,
            shape="rectangle",
            style="filled,bold",
            fillcolor="lightblue",
            fontsize="14",
            fontname="Helvetica",
            margin="0.3"
        )

    # =====================================================
    # Create Sequence Edges
    # =====================================================

    for idx, (source, target, command) in enumerate(interactions):

        dot.edge(
            source,
            target,
            label=f"{idx + 1}: {command}",
            fontsize="12",
            fontname="Helvetica",
            arrowsize="0.8"
        )

    return dot


# =========================================================
# Streamlit Page Config
# =========================================================

st.set_page_config(
    page_title="AI TANGO Engineering System",
    layout="wide"
)

st.title("AI Multi-Agent TANGO Engineering System")

st.markdown(
    "AI-assisted TANGO feature development using multi-agent workflow."
)

# =========================================================
# User Requirement Input
# =========================================================

user_requirement = st.text_area(
    "Enter Feature Requirement",
    height=250,
    placeholder="""
Example:

Implement TelescopeON command orchestration.

Requirements:
- TelescopeON invoked on CentralNode
- CentralNode invokes TelescopeON on CSPMaster and SDPMaster
- Wait for ResultCode.OK from all devices
- Return FAILED if any device fails
"""
)

# =========================================================
# Generate Workflow
# =========================================================

if st.button("Generate"):

    orchestrator = WorkflowOrchestrator()

    with st.spinner("AI Agents Processing..."):

        result = orchestrator.run(user_requirement)

    # =====================================================
    # Tabs
    # =====================================================

    tab1, tab2, tab3, tab4 = st.tabs([
        "Requirements",
        "Architecture",
        "Sequence Diagram",
        "Generated Devices"
    ])

    # =====================================================
    # Requirements Tab
    # =====================================================

    with tab1:

        st.subheader("Structured Requirements")

        st.json(result["requirement_output"])

    # =====================================================
    # Architecture Tab
    # =====================================================

    with tab2:

        st.subheader("AI Generated Architecture")

        st.markdown(result["architecture_output"])

    # =====================================================
    # Sequence Diagram Tab
    # =====================================================

    with tab3:

        st.subheader(
            "AI Generated Flow Diagram"
        )

        diagram = build_sequence_diagram(
            result["architecture_output"]
        )

        st.graphviz_chart(
            diagram,
            use_container_width=True
        )

    # =====================================================
    # Generated Devices Tab
    # =====================================================

    with tab4:

        st.subheader(
            "Generated TANGO Device Code"
        )

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