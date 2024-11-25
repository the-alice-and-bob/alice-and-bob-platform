from urllib.parse import urlparse


def check_site(site: str) -> str:
    """
    This function checks if the site is valid.

    :return: the site domain and protocol
    """

    if not site:
        raise ValueError("Site is required")

    # check that is a valid URL
    try:
        parsed = urlparse(site)
    except ValueError:
        raise ValueError(f"Invalid site: {site}")

    if not parsed.netloc:
        raise ValueError(f"Invalid site: {site}")

    if not parsed.scheme:
        raise ValueError(f"Invalid site: {site}")

    if parsed.scheme not in ["http", "https"]:
        raise ValueError(f"Invalid site: {site}")

    return f"{parsed.scheme}://{parsed.netloc}"


__all__ = ("check_site",)
