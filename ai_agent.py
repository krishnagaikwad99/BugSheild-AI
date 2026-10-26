
import os

import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.groq import Groq


def get_groq_api_key():
    """Read the Groq API key locally or from Streamlit Cloud."""
    load_dotenv()

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        try:
            api_key = st.secrets["GROQ_API_KEY"]
        except Exception:
            api_key = None

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to your .env file "
            "or configure it in Streamlit Cloud Secrets."
        )

    os.environ["GROQ_API_KEY"] = api_key
    return api_key


def build_testing_agent():
    """Create the Agentic AI software testing assistant."""
    get_groq_api_key()

    return Agent(
        name="Agentic AI Testing Assistant",
        model=Groq(id="openai/gpt-oss-120b"),
        instructions=[
            "You are an expert Python software testing assistant.",
            "Analyze the provided Python code carefully.",
            "Identify potential bugs and explain why they occur.",
            "Suggest clear, practical fixes.",
            "Generate relevant pytest test cases when requested.",
            "Include edge cases and invalid inputs where appropriate.",
            "Use simple language and format your response with headings.",
            "Do not claim that tests were executed unless they actually were.",
        ],
        markdown=True,
    )


def analyze_code(code: str) -> str:
    """Analyze code and return the AI-generated response."""
    if not code or not code.strip():
        return "Please provide Python code to analyze."

    try:
        agent = build_testing_agent()

        response = agent.run(
            "Analyze this Python code for potential bugs. "
            "Explain the issues, suggest fixes, and provide pytest "
            "test cases.\n\n"
            "```python\n"
            f"{code}\n"
            "```"
        )

        content = getattr(response, "content", None)

        if content:
            return str(content)

        return str(response)

    except Exception as error:
        return (
            "AI analysis failed. Please check your Groq API key, "
            "model availability, and application logs.\n\n"
            f"Error: {error}"
        )
