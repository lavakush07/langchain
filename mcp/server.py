"""MCP server that exposes LangChain capabilities as tools, resources, and prompts."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from dotenv import load_dotenv
from fastmcp import FastMCP
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
mcp = FastMCP("langchain-ai-server")

PAPER_SUMMARY_TEMPLATE = PromptTemplate(
    template="""
Please summarize the research paper titled "{paper_input}" with the following specifications:
Explanation Style: {style_input}
Explanation Length: {length_input}
1. Mathematical Details:
   - Include relevant mathematical equations if present in the paper.
   - Explain the mathematical concepts using simple, intuitive code snippets where applicable.
2. Analogies:
   - Use relatable analogies to simplify complex ideas.
If certain information is not available in the paper, respond with: "Insufficient information available" instead of guessing.
Ensure the summary is clear, accurate, and aligned with the provided style and length.
""",
    input_variables=["paper_input", "style_input", "length_input"],
    validate_template=True,
)


@mcp.tool()
def generate_prompt(paper_input: str, style_input: str, length_input: str) -> str:
    """Build a research-paper summary prompt from the configured template.

    Args:
        paper_input: Title or topic of the research paper.
        style_input: Explanation style, e.g. technical or beginner-friendly.
        length_input: Desired summary length, e.g. short, medium, or long.
    """
    return PAPER_SUMMARY_TEMPLATE.format(
        paper_input=paper_input,
        style_input=style_input,
        length_input=length_input,
    )


@mcp.tool()
def chat(message: str, model: str = "gpt-4o-mini") -> str:
    """Send a message to a LangChain chat model and return the response.

    Args:
        message: User message to send to the model.
        model: OpenAI model name to use for the response.
    """
    llm = ChatOpenAI(model=model, temperature=0)
    response = llm.invoke(message)
    return response.content


@mcp.tool()
def generate_embedding(text: str, dimensions: int = 32) -> list[float]:
    """Generate a vector embedding for the given text.

    Args:
        text: Input text to embed.
        dimensions: Embedding vector size (default: 32).
    """
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        dimensions=dimensions,
    )
    return embeddings.embed_query(text)


@mcp.tool()
def run_chain(topic: str) -> str:
    """Run the LangChain prompt | model | parser chain for a sports team topic.

    Args:
        topic: Team name or topic passed into the chain template.
    """
    prompt = PromptTemplate(
        template="Generate five players of the team {topic} ",
        input_variables=["topic"],
    )
    model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    parser = StrOutputParser()
    chain = prompt | model | parser
    return chain.invoke({"topic": topic})


@mcp.resource("langchain://config")
def get_config() -> str:
    """Application configuration and available LLM providers."""
    config_path = PROJECT_ROOT / "mcp-config.json"
    if config_path.exists():
        return config_path.read_text(encoding="utf-8")
    return json.dumps({"name": "langchain-ai-server", "status": "running"})


@mcp.resource("langchain://template/paper-summary")
def get_paper_summary_template() -> str:
    """The paper summary prompt template used by the prompt-generator tool."""
    template_path = PROJECT_ROOT / "prompts" / "template.json"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return PAPER_SUMMARY_TEMPLATE.template


@mcp.prompt()
def paper_summary(
    paper_input: str,
    style_input: str = "technical",
    length_input: str = "medium",
) -> str:
    """Prompt template for summarizing a research paper."""
    return PAPER_SUMMARY_TEMPLATE.format(
        paper_input=paper_input,
        style_input=style_input,
        length_input=length_input,
    )


if __name__ == "__main__":
    mcp.run(transport="stdio")
