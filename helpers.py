from bs4 import BeautifulSoup
import wikipedia as wiki
import re
import time

def get_page(query):
    search = wiki.search(query)
    try:
        page = wiki.WikipediaPage(search[0])
    except wiki.exceptions.DisambiguationError:
        page = wiki.WikipediaPage(search[1])
    except wiki.exceptions.PageError:
        return None
    return page


def get_links(page_name):
    # disambiguation
    try:
        page = wiki.WikipediaPage(page_name)
        return parse_links(page)
        #return wiki.WikipediaPage(page_name).links
    except wiki.exceptions.DisambiguationError as de:
        return de.options
    except wiki.exceptions.PageError:
        return None
    pass


def get_links2(page_name):
    # disambiguation
    try:
        return wiki.WikipediaPage(page_name).links
    except wiki.exceptions.DisambiguationError as de:
        return de.options
    except wiki.exceptions.PageError:
        return None
    pass


def timelen(page):
    tic = time.perf_counter()
    print(len(get_links(page)))
    toc = time.perf_counter()
    print(f"BS Found links in {toc - tic:0.4f} seconds")
    tic1 = time.perf_counter()
    print(len(get_links2(page)))
    toc1 = time.perf_counter()
    print(f"Wiki Found links in {toc1 - tic1:0.4f} seconds")

def is_disamb(page_name):
    try:
        wiki.WikipediaPage(page_name)
    except wiki.exceptions.DisambiguationError:
        return True
    except wiki.exceptions.PageError:
        return False
    return False


def is_page(page_name):
    try:
        wiki.WikipediaPage(page_name)
    except wiki.exceptions.PageError:
        return False
    return True


def has_end(page, end_page):
    return end_page.title in page.links


def parse_links(page):
    main_html = BeautifulSoup(page.html(), "html.parser")
    ref_html = main_html.find_all(name="div", attrs={"class": "reflist"})[0]
# 'Jean Lanfray' Absinthe 

    # switch case dict
    # ref_links = {0:[name="div", attrs={"class": "reflist" }] 



    main_str = str(main_html)
    references_str = str(ref_html)
    references_idex = main_str.find(references_str)
    page_content = main_str[:references_idex]

    content_soup = BeautifulSoup(page_content, "html.parser")
    all_links = content_soup.find_all(
        name="a", attrs={"class": None, "title": re.compile(".")})  # results set
    return get_titles(all_links)
    

def get_titles(all_links):
    links = set()
    edit_links = set()
    for link in all_links:
        # print(link)
        # print(link["title"])
        if re.search("^Edit section:", link["title"]):
            # print(link["title"])
            edit_links.add(link["title"])
        elif re.search("^Wikipedia:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Template:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Portal:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Help:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Talk:", link["title"]):
            edit_links.add(link["title"])
        else:
            links.add(link["title"])


    # print(pg.title)
    # print("-----------------------------")
    return links - edit_links
    # for link in links:
        # print(link["title"])
        # print(link)