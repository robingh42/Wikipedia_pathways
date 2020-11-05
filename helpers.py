from bs4 import BeautifulSoup
import wikipedia as wiki
from pathlib import Path
import re
import time


def get_page(query):
    search = wiki.search(query)
    link_num = 0
    if search == []:
        print(f"*Error gettin page: {query}*")
        print("Check your spelling, and if the page exists.")
        return None
    while is_disamb(search[link_num]) and link_num < len(search):
        link_num += 1
    try:
        page = wiki.WikipediaPage(search[link_num])
    except wiki.exceptions.DisambiguationError:
        return None
    except wiki.exceptions.PageError:
        return None
    return page


def get_links(page_name):
    # disambiguation
    if is_stored(page_name):
            print("Page stored!")
            return read_links(page_name)
    else:
        try:
            page = wiki.WikipediaPage(page_name)
            links = parse_links1(page)
            save_links(page_name, links)
            return links
            #return wiki.WikipediaPage(page_name).links
        except wiki.exceptions.DisambiguationError as de:
            return de.options
        except wiki.exceptions.PageError:
            return None
        pass


def read_links(title):
    with open(f"link_data/{title}", "r") as f:
        read_data = f.read()
        return read_data.split("\n")[:-1]


def save_links(title, links):
    if title.find("/") != -1:
        return False
    with open(f"link_data/{title}", "w") as f:
        for link in links:
            f.write(link + "\n")
        return True


def timelen(page_name):
    tic = time.perf_counter()
    print(len(get_links(page_name)))
    toc = time.perf_counter()
    print(f"Found links in {toc - tic:0.4f} seconds")
    

def is_stored(title):
    return Path(f"link_data/{title}").is_file()


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


def has_end(page_title, end_page):
    return end_page.title in get_links(page_title)


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


def parse_links1(page):
    main_html = BeautifulSoup(page.html(), "html.parser")
    args = [
        ["div", {"class": "reflist"}],
        ["div", {"class": "mw-references-wrap"}],
        ["span", {"id": "References"}],
        ["span", {"id": "Sources"}],
        ["span", {"id": "External_links"}],
        ["div", {"class": "navbox"}],
        ["table", {"id": "disambigbox"}],
        ["table", {"id": "setindexbox"}],
        ]
    args_opt = 0
    ref_html = main_html.find_all(name=args[args_opt][0], attrs=args[args_opt][1])
    #print(ref_html)
    while ref_html == [] and args_opt < len(args) -1:
        args_opt += 1
        ref_html = main_html.find_all(name=args[args_opt][0], attrs=args[args_opt][1])

    if ref_html == []:
        print(f"*Wiki format error or page stub* {page.title}")
        return page.links
    else: 
        ref_html = ref_html[0]

    main_str = str(main_html)
    references_str = str(ref_html)
    references_idex = main_str.find(references_str)
    page_content = main_str[:references_idex]

    content_soup = BeautifulSoup(page_content, "html.parser")
    all_links = content_soup.find_all(
        name="a", attrs={"class": None, "title": re.compile(".")}
        )  # results set
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
        elif re.search("^Help:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Talk:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Template:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^File:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Template talk:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Special:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Category:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Portal:", link["title"]):
            edit_links.add(link["title"])
        elif re.search("^commons:",link["title"]):
            edit_links.add(link["title"])
        elif re.search("^Commons:",link["title"]):
            edit_links.add(link["title"])
        else:
            links.add(link["title"])


    # print(pg.title)
    # print("-----------------------------")
    return links - edit_links
    # for link in links:
        # print(link["title"])
        # print(link)