from ezycourse.sdk.utils import extract_og


if __name__ == '__main__':
    # url = "https://www.alicebob.io/es"
    url = "https://vulners.com/cve/CVE-2024-10407?utm_source=rss&utm_medium=rss&utm_campaign=rss"
    og = extract_og(url)

    print(og)
