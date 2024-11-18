from enum import Enum
from typing import List, Tuple

import orjson

import ollama

from ..models import NewsTags
from .prompts import GLOBAL_PROMPT


class OLlamaModeles(Enum):
    LLAMA_3_2 = "llama3.2"
    LLAMA_3_1 = "llama3.1"


def generate_summary(
        text,
        additional_prompt: str = "",
        *,
        model: OLlamaModeles = OLlamaModeles.LLAMA_3_1
) -> Tuple[List[NewsTags], str, str, dict or None]:

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

    message_01 = ollama.chat(
        messages=[
            {
                "role": "user",
                "content": prompt,
            },
        ],
        model=model.value,
    )

    response = message_01["message"]["content"]

    try:
        data = orjson.loads(response)
    except orjson.JSONDecodeError:
        raise ValueError("Invalid JSON data")

    tags = [NewsTags(x) for x in data.pop("tags", [])]
    linkedin = data.pop("linkedin", "")
    twitter = data.pop("twitter", "")

    return tags, linkedin, twitter, data
