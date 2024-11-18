import base64
import os

from anthropic import Anthropic


API_KEY = "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"

MIN_PALABRAS = 100
MAX_PALABRAS = 150

PROMPT = f"""
Eres un experto en seguridad y experto copywriter. Quiero que resumas contenido técnico de diferentes fuentes, normalmente webs.

Quieren que hagas un resumen de {MIN_PALABRAS}-{MAX_PALABRAS} palabras para publicarlo en LinkedIn. El resumen tiene que hacer referencia al contenido de otra persona. No hables de ti mismo.

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


def dividir_texto(texto, tamaño_bloque=8000):
    # Divide el texto en bloques de 'tamaño_bloque' caracteres
    bloques = [texto[i:i + tamaño_bloque] for i in range(0, len(texto), tamaño_bloque)]
    return bloques


def main():
    with open("content.txt", "r") as f:
        content = f.read()

    b64_content = base64.b64encode(content.encode()).decode()

    bloques = dividir_texto(content)

    client = Anthropic(
        # This is the default and can be omitted
        api_key=API_KEY,
    )

    prompt = f"""{PROMPT}

ESTE ES EL CONTENIDO QUE DEBES RESUMIR:

{content}

Ahora haz el resumen. Dame solo el texto, sin saludos ni despedidas. Solo el resumen.
"""

    model = "claude-3-haiku-20240307"
    model = "claude-3-opus-20240229"
    model = "claude-3-sonnet-20240229"
    model = "claude-3-5-sonnet-latest"

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
            model=model,
        )

    print(message_01.content[0].text)


if __name__ == '__main__':
    main()
