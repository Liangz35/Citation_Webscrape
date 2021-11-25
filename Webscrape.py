from bs4 import BeautifulSoup
import re
import requests

def URL_to_intext(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    authors = soup.find_all("a", class_ = "full-name")
    authors = [author.text.strip() for author in authors]
    main_author = authors[0].split(' ')[-1]

    publication = soup.find("span", class_ = "cit")
    publication = publication.text.strip()
    publication_year = re.findall('[0-9]+',publication)[0]

    if len(authors) > 1:
        return "(" + main_author + " et al., " + publication_year + ")"
    else:
        return "(" + main_author + ", " + publication_year + ")"


def document_citation(document: str, delimiter: str = "[]"):

    if len(delimiter)%2 != 0:
        raise Exception("Please enter a symmetrical delimiter")

    first = delimiter[:int(len(delimiter)/2)]
    second = delimiter[int(len(delimiter)/2):]
    document_cite = document
    # For all the matches
    URLs = []
    # Iterate the whole file
    start = document.find(first)
    end = document.find(second)

    while start != -1 and end != -1:
        URLs.append(document[start+len(first):end])
        document = document[end+len(second):]
        start = document.find(first)
        end = document.find(second)

    if len(URLs) != 0:
        for URL in URLs:
            URL_replace = first + URL + second
            document_cite = document_cite.replace(URL_replace, URL_to_intext(URL))
    else:
        pass

    return document_cite




