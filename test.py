from helpers import *
from bs4 import BeautifulSoup
import wikipedia as wiki

def test1():
    page = get_page(wiki.random())
 

    print(page.title)

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
        print(f"*Wiki format error* {page.title}")
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
    print(len(get_titles(all_links)))
    #return get_titles(all_links)


print("how many times:")
x = int(input())

for i in range(x):
    test1()
