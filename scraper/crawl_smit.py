import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from langchain_core.documents import Document

BASE_URL = "https://www.smu.edu.in/smit"

visited = set()


def clean_text(text):
    return " ".join(text.split())


def crawl(url, max_pages=100):

    docs = []

    queue = [url]

    while queue and len(visited) < max_pages:

        current = queue.pop(0)

        if current in visited:
            continue

        try:
            response = requests.get(current, timeout=10)

            soup = BeautifulSoup(response.text, "html.parser")

            visited.add(current)

            text = clean_text(soup.get_text(separator=" "))

            docs.append(
                Document(
                    page_content=text,
                    metadata={"source": current}
                )
            )

            for link in soup.find_all("a"):

                href = link.get("href")

                if not href:
                    continue

                absolute_url = urljoin(BASE_URL, href)

                if absolute_url.startswith(BASE_URL):

                    if absolute_url not in visited:
                        queue.append(absolute_url)

        except Exception as e:
            print(e)

    return docs


if __name__ == "__main__":

    docs = crawl(BASE_URL)

    print(len(docs))