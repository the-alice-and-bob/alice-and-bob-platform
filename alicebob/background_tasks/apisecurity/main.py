from typing import Iterable, List

from lxml import html

from alicebob.sdk import News, SummarizedNews, summarize_with_ia, find_news


def extract_news(news) -> Iterable[str]:

    # Parseamos el contenido
    tree = html.fromstring(news.summary)

    # Inicializamos la lista de resultados y variables temporales
    result = []
    current_section = None
    current_content = []

    # Iteramos sobre cada elemento en el HTML
    for elem in tree.iter():
        # Cuando encontramos un h2, guardamos la sección anterior y creamos una nueva
        if elem.tag == 'h2':
            if current_section is not None and current_content:
                result.append({current_section: current_content})
            current_section = elem.text_content().strip() if elem.text_content() else "Sin título"
            current_content = []
        # Añadimos <p> hasta que encontremos <ul>
        elif elem.tag == 'p' and current_section:
            current_content.append(html.tostring(elem, encoding='unicode').strip())
        elif elem.tag == 'ul' and current_section:
            # Agregamos la última sección al resultado y detenemos la extracción
            if current_content:
                result.append({current_section: current_content})
            break

    # Añadimos cualquier contenido restante si existe
    if current_section is not None and current_content:
        result.append({current_section: current_content})

    # Merge all the content
    for item in result:
        title = list(item.keys())[0]
        content = "\n".join(list(item.values())[0])
        yield title, content


def main(news: News) -> List[SummarizedNews]:

    # Extraemos el contenido de la noticia
    #
    additional_prompt = f"""
En JSON de respuesta, añade un campo con la URL de la noticia original. El campo se llamará "url" y contendrá la URL de la noticia original. E irá después de los tags.
"""

    print(f"[*] Processing API Security news: {news.title}")
    for (title, content) in extract_news(news):

        if find_news(news) > 0:
            print(f"[!] News already processed: {news.title}")
            continue

        data_for_prompt = f"{title}\n\n{content}"

        tags, linkedin, twitter, other = summarize_with_ia(data_for_prompt, additional_prompt=additional_prompt)

        reference_url = other.get("url", None) or news.origin

        yield SummarizedNews(
            title=title,
            linkedin=linkedin,
            twitter=twitter,
            tags=tags,
            url=reference_url,
            published=news.published,
            provider=news.provider.name.lower(),
            origin=news.origin
        )


