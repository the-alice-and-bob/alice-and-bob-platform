import re
import json

from enum import Enum
from datetime import datetime
from dataclasses import dataclass
from typing import List, Iterable, Tuple, Dict

import requests
import html2text_rs

from anthropic import Anthropic

from notion_client import Client

URL_TOKEN = "uef7b36135154447faf16d6a8ff19b0c12605d0eae16144399165aa1edf7e1c5d"

NOTION_API_KEY = "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"
NOTION_DATABASE_ID = "12e9eddc9f9c8067abaddc798615c212"

OPENAI_API_KEY = "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"
ANTHROPIC_API_KEY = "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"

SUMMARY_MIN_PALABRAS = 100
SUMMARY_MAX_PALABRAS = 150

GLOBAL_PROMPT = f"""
Eres un experto en seguridad y experto copywriter. Quiero que resumas contenido técnico de diferentes fuentes, normalmente webs.

Quieren que hagas un resumen de {SUMMARY_MIN_PALABRAS}-{SUMMARY_MAX_PALABRAS} palabras para publicarlo. El resumen tiene que hacer referencia al contenido de otra persona. No hables de ti mismo.

El resumen quiero que me lo des en 2 formatos: 

- Para LinkedIn (puede tener hasta {SUMMARY_MAX_PALABRAS} palabras)
- Para twitter (puede tener hasta 280 caracteres). Este tiene que ser informal e impactante.

No lo pongas todo en una sola linea. Usa frases cortas. Separa párrafos.

USA ESTE ESTILO DE ESCRITURA:

Quiero que el texto resumen me lo escribas en español. Pero no hagas una traducción literal.

Que suene como si estuviera hablando directamente con el lector, en un tono natural y cercano, evitando palabras rimbombantes o el estilo formal de un correo electrónico.

Usa un lenguaje sencillo y directo, como en una conversación cara a cara. Mezcla frases cortas y largas para darle ritmo, y añade algunas expresiones coloquiales o muletillas que suenen auténticas, como ‘Ojo’, ‘Así de simple’, ‘Para que lo tengas claro’, y cualquier otra que dé el toque de un lenguaje humano y accesible.

Haz que el lector sienta que está hablando con alguien que entiende y explica sin vueltas. Mantén una estructura que invite a seguir leyendo.

Quiero que trates de copiar mi tono de escritura. Te adjunto ejemplos de correos electrónicos que yo envío para que copies mi estilo.

EJEMPLOS:
--
Ey!
Nos habéis escribo bastantes sobre la charla de Dani (cr0hn) Navaja Negra 2024.
La verdad es que es un subidón, para que os vamos a engañar :)
El tema:
Hay mogollón de preguntas que nos hacéis.
Como contestar una por una es un rollo, Dani va a hacer una sesión en directo de preguntas y respuestas.
Os podéis apuntar aquí:
https://www.alicebob.io/es/optin-3f78da70-7546-447a-b8a3-7376777106bf
» SOLO HAY 50 plazas «
En 1 hora lo publicaremos también en redes sociales para que se apunte la gente. Te lo mando a ti primero por haberme dado tu email para que avisara de cosas de la charla.
Si te quieres apuntar, date prisa.
En 1 hora
Chau!
—-
Ea.
Me ha costado un poco, no te voy a engañar.
Ya puedes descargar las transparencias de mi charla de Navaja Negra 2024.
He retocado las transparencias y he sacado los videos para que los podáis ver a parte.
Las he puesto en la Comunidad de Alice & Bob: Seguridad y otras yerbas. En el canal de Eventos.
> > > VER TRANSPARENCIAS
Todavía no he podido recopilar el material adicional, lo siento. He estado más liado que la pata de un romano.
Prometo enviarte lo que queda.
De momento, cualquier pregunta que te quedaras con ganas de hacerme puedes dejar un comentario y la responderé. Lo prometo. Cuando me de la vida.
No vemos.
—-
Bueno.
La verdad es que es jodido.
Sí, es bastante jodido.
El sábado pasado di mi charla en Navaja Negra sobre cómo fastidiar a un DBA.
Me preguntaron mucho al salir y durante el resto del evento.
La pregunta era siempre la misma:
¿Cómo narices detecto los ataques que has comentado?
Pues siento decirte que para la charla solo pensé cómo hacer el mal y no me plantee otra cosa.
Que puedan exfiltrar datos de tu base de datos sin que el SIEM de turno se entere de una mierda es una putada, todo hay que decirlo.
Te voy a ser honesto:
Todavía no he pensado en ello y no me corre mucha prisa, la verdad.
Si te corre prisa escríbeme y le damos una vuelta a ver.
Las transparencias ya las tengo listas, a ver si me da tiempo a subirlas y te aviso.
Un saludo
—
FIN DE LOS CORREOS DE PRUEBA
—-

"""




def check_token(event: dict):
    try:
        token = event["token"]
    except KeyError:
        raise ValueError("Missing token in the request")

    if token != URL_TOKEN:
        raise ValueError("Invalid token")





# -------------------------------------------------------------------------
# New providers
# -------------------------------------------------------------------------




# Provider :: API_SECURITY


if __name__ == '__main__':
    # filename = "inoreader-api-security.json"
    filename = "inoreader-01.json"

    # here = os.path.dirname(os.path.abspath(__file__))
    request_data = {
        "body": json.load(open("inoreader-03.json")),
        "headers": {
            "Content-Type": "application/json"
        },
        "token": "uef7b36135154447faf16d6a8ff19b0c12605d0eae16144399165aa1edf7e1c5d",
        "method": "POST",
    }

    query_url = "https://faas-ams3-2a2df116.doserverless.co/api/v1/web/fn-d3c5b8e2-cbcd-4c8d-833d-8bb36e317589/alicebob/inoreader?blocking=false&result=false"

    response = requests.post(query_url, json=request_data, headers={
        "Content-Type": "application/json",
        # "X-Require-Whisk-Auth": "Fh7CVSeRooVuQym"
        "X-Require-Whisk-Auth": "Fh7CVSeRooVuQym"
    })

    print(response.headers)
    print(response.text)
    # print(json.dumps(request_data))
    # print(request_data)
#
#     print(main(request_data, None))
