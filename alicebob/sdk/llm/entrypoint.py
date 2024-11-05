import decouple

from typing import Tuple, List

from ..models import NewsTags
from .ollama import generate_summary as generate_summary_ollama
from .anthropic import generate_summary as generate_summary_anthropic


def summarize_with_ia(
        text: str, additional_prompt: str = "", *, model: str = "claude-3-5-sonnet-latest"
) -> Tuple[List[NewsTags], str, str, dict or None]:
    """
    Generate a summary using the Anthropic API.

    :param text: Text to summarize
    :param additional_prompt: Additional prompt to include in the request
    :param model: Model to use
    """
    return [], "", "", {}

    llm_engine = decouple.config("LLM_ENGINE", default="anthropic")

    if llm_engine == "anthropic":
        return generate_summary_anthropic(text, additional_prompt=additional_prompt)

    elif llm_engine == "ollama":
        return generate_summary_ollama(text, additional_prompt=additional_prompt)

    raise ValueError(f"Invalid LLM engine: {llm_engine}")


__all__ = ("summarize_with_ia",)
