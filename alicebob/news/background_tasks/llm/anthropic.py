from enum import Enum
from typing import List, Tuple

import orjson
import decouple

from anthropic import Anthropic

from ..models import NewsTags
from .prompts import GLOBAL_PROMPT


class AnthropicModeles(Enum):
    HAUKU = "claude-3-haiku-20240307"
    OPUS = "claude-3-opus-20240229"
    SONNET = "claude-3-sonnet-20240229"
    SONNET_LATEST = "claude-3-5-sonnet-latest"


def generate_summary(
        text,
        additional_prompt: str = "",
        *,
        model: AnthropicModeles = AnthropicModeles.SONNET_LATEST
) -> Tuple[List[NewsTags], str, str, dict or None]:

    client = Anthropic(
        # This is the default and can be omitted
        api_key=decouple.config("ANTHROPIC_API_KEY"),
    )

    prompt = f"""{GLOBAL_PROMPT}

ESTE ES EL CONTENIDO QUE DEBES RESUMIR:

{text}

{additional_prompt}

También quiero que me identifiques los tags. Estos son los tags que puedes usar. No es necesario que uses todos, solo los que consideres relevantes: Hasta 3.

{', '.join(NewsTags.tags())}

Ahora haz el resumen. Dame solo el resultado, sin saludos ni despedidas. Solo el resumen.

Dámelo en el siguiente formato JSON. El contenido del campo "resumen" será en texto plano. Escapando las comillas dobles y teniendo cuidado con los saltos de línea. 

{{
    "linkedin": <string>
    "twitter": <string>
    "tags": <list>
}}
"""
    print("[!] Generating summary with Anthropic")

    message_01 = client.messages.create(
        max_tokens=2500,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt,
                    }
                ]
            },
        ],
        model=model.value,
    )

    response = message_01.content[0].text

    try:
        data = orjson.loads(response)
    except orjson.JSONDecodeError:
        raise ValueError("Invalid JSON data")

    tags = [NewsTags(x) for x in data.pop("tags", [])]
    linkedin = data.pop("linkedin", "")
    twitter = data.pop("twitter", "")

    return tags, linkedin, twitter, data
