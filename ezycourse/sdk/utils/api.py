from typing import Iterable

import requests


def iterate_endpoint(
        url: str, method: str, headers: dict, query_params: dict, data: dict | None = None, stop_page: int | None = None
) -> Iterable[dict]:
    """
    Iterate over paginated API endpoint and yield data

    :param url: API endpoint URL
    :param method: HTTP method
    :param headers: HTTP headers
    :param query_params: Query parameters
    :param data: JSON data
    :param stop_page: Stop iteration
    :return: the json response from the API
    """

    # Set default query params for pagination
    query_params.update({
        "page": 1,
        "per_page": 100,
    })

    if stop_page and stop_page < 1:
        raise ValueError("stop_page must be greater than 0")

    # Iterate over all pages
    fn = getattr(requests, method.lower())

    if method == "GET":
        config = {
            "url": url,
            "headers": headers,
            "params": query_params
        }
    else:
        config = {
            "url": url,
            "headers": headers,
            "params": query_params,
            "json": data
        }

    response = fn(**config)

    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.text}")

    data = response.json()

    yield data

    if stop_page and stop_page == 1:
        return

    total_pages = stop_page = response.json()["meta"]["last_page"]
    current_page = response.json()["meta"]["current_page"]

    while current_page < total_pages and current_page < stop_page:
        query_params["page"] = current_page + 1
        response = fn(**config)
        data = response.json()
        yield data
        current_page = data["meta"]["current_page"]


__all__ = ("iterate_endpoint", )
