from bs4 import BeautifulSoup
import re
import requests
import streamlit as st

@st.cache()
def URL_to_intext(URL):

    if "https://pubmed.ncbi.nlm.nih.gov/" in URL:
        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
        except:
            pass
        authors = soup.find_all("a", class_ = "full-name")
        authors = [author.text.strip() for author in authors]
        main_author = authors[0].split(' ')[-1]

        publication = soup.find("span", class_ = "cit")
        publication = publication.text.strip()
        publication_year = re.findall('[0-9]+',publication)[0]

        if len(list(set(authors))) > 1:
            return "(" + main_author + " et al., " + publication_year + ")"
        else:
            return "(" + main_author + ", " + publication_year + ")"


    if "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC" in URL:
        if "figure" in URL:
            URL = URL.split('figure')[0]

        try:
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
        except:
            pass




        try:
            authors = soup.find_all("div", class_ = "half_rhythm")
            authors = [author.text.strip() for author in authors]
            authors = authors[0]
            authors = authors.split(',')


            main_author = authors[0].split(" ")[-1]
            #main_author = ''.join([letter for letter in main_author if letter.isalpha])
            main_author = "".join(re.findall("[a-zA-Z]+", main_author))

            publication = soup.find("span", class_="fm-vol-iss-date")
            publication = publication.text.strip()
            publication_year = re.findall('[0-9]+', publication)[0]
        except IndexError:
            return None


        if len(list(set(authors))) > 1:
            return "(" + main_author + " et al., " + publication_year + ")"
        else:
            return "(" + main_author + ", " + publication_year + ")"



@st.cache()
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
            intext = URL_to_intext(URL)
            if intext != None:
                document_cite = document_cite.replace(URL_replace, intext)

    else:
        pass

    return document_cite




