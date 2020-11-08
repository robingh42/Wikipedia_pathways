from bs4 import BeautifulSoup
import wikipedia as wiki
from pathlib import Path
import re


def get_page(query):
    """
    Returns a Wikipedia Page Object from a search term.

    Assumes the page esists and the query is mostly spelled right

    Args:
        query: (Str) The title of wiki page to search for

    Returns Wikipedia Page Object
    """
    # Get a list of article titles based on the search query
    search = wiki.search(query)
    link_num = 0
    # Check if search is empty and return none with an error message
    if search == []:
        print(f"*Error getting page: {query}*")
        print("Check your spelling, and if the page exists.")
        return None
    # if the page is a disambiguation page return the first valid link
    while is_disamb(search[link_num]) and link_num < len(search):
        link_num += 1
    # otherwise return a vailid Wikipedia Page or None
    try:
        page = wiki.WikipediaPage(search[link_num])
    except wiki.exceptions.DisambiguationError:
        return None
    except wiki.exceptions.PageError:
        return None
    return page


def get_links(page_name):
    """
    Returns all the links in a wikipedia article.

    Args:
        page_name: (Str) The title of the current wiki page

    Returns a list of all the links in the wiki article
    """
    # Check if the articles' links are save in a file and return those links
    if is_stored(page_name):
        return read_links(page_name)

    # Parse the HTML for links, save them to a file, and return links
    else:
        try:
            page = wiki.WikipediaPage(page_name)  # Get the wikipedia page
            links = parse_links(page)
            if links != []:
                print("Page stored to a file:")
                save_links(page_name, links)
            return links

        # If the page is a disambiguation return the links within it
        except wiki.exceptions.DisambiguationError as de:
            return de.options
        except wiki.exceptions.PageError:
            return None
        pass


def read_links(title):
    """
    Reads the links from a file in directory link_data.

    Assumes the file exists, as well as the directory link_data

    Args:
        title: (Str) The title of the current wiki file to read

    Returns a list of all the links in the wiki article with the name title
    """
    with open(f"link_data/{title}", "r") as f:
        read_data = f.read()
        return read_data.split("\n")[:-1]


def save_links(title, links):
    """
    Saves the links to a file for easy access.

    Assumes the directory link_data

    Args:
        title: (Str) The title of the current wiki article to save as a file
        links: (List) List of all the links in the wikipedia article

    Returns true is the the file is created, false if is not created
    """
    # If the article title has a "/" in it, do not save it as a file
    # Otherwise the program throws an error
    if title.find("/") != -1:
        return False
    # Open a file in the directory linkdata with the file name "title"
    # and save all the links in the file
    with open(f"link_data/{title}", "w") as f:
        for link in links:
            f.write(link + "\n")
        return True


def is_stored(title):
    """
    Checks if the file for the page exists, returning a Boolean

    Args:
        title: (Str) The title of the current file to check

    Returns true is the file exists, false if it does not
    """
    return Path(f"link_data/{title}").is_file()


def is_disamb(page_name):
    """
    Checks if the page is a disambiguation page, returning a Boolean

    Args:
        page_name: (Str) The title of the current page to check

    Returns true is the page is a disambiguation, false if it does not
    """
    try:
        wiki.WikipediaPage(page_name)
    except wiki.exceptions.DisambiguationError:
        return True
    except wiki.exceptions.PageError:
        return False
    return False


def is_page(page_name):
    """
    Checks if the page exists, returning a Boolean

    Args:
        page_title: (Str) The title of the current page to check

    Returns true is the page exists, false if it does not
    """
    try:
        wiki.WikipediaPage(page_name)
    except wiki.exceptions.PageError:
        return False
    except wiki.exceptions.DisambiguationError:
        return True
    return True


def has_end(page_title, end_page):
    """
    Searches the links in a page for the end page.

    Args:
        page_title: (Str) The title of the current page to search
        end_page: (Wikipedia Page) The last page we are searching for.

    Returns a true if the current page has the end page in its links
        otherwise returns false
    """
    return end_page.title in get_links(page_title)


def parse_links(page):
    """
    Takes a Wikipedia Page and returns a list of the links inside of it.

    Expects a valid Wikipedia Object, if the page is a stub or improperly
        formated will default to the .links funtion in Wikipedia library
    Uses Beautiful soup to scrap wikipedia HTML and then uses get_titles
        to only grab relevant titles

    Args:
        Page: (Wikipedia Page) A Wikipedia Page Object to find all the links in

    Returns a list of links without any "Meta" wiki links
    """
    # Get the pages' HTML and parse it with Beautiful Soup
    main_html = BeautifulSoup(page.html(), "html.parser")
    # A list of all the refference section labels
    # Only one of these will be used, but a list is needed
    # as wikipedia pages are configured in many ways

    args = [
        ["div", {"class": "mw-references-wrap"}],
        ["span", {"id": "References"}],
        ["span", {"id": "Sources"}],
        ["span", {"id": "External_links"}],
        ["div", {"class": "navbox"}],
        ["table", {"id": "disambigbox"}],
        ["table", {"id": "setindexbox"}],
        ["div", {"class": "reflist"}]]
    args_opt = 0
    # try to get the reference section using the first argument in the list
    ref_html = main_html.find_all(
        name=args[args_opt][0],
        attrs=args[args_opt][1])
    # if that returns empty try each argument till one returns not empty
    while ref_html == [] and args_opt < len(args) - 1:
        args_opt += 1
        ref_html = main_html.find_all(
            name=args[args_opt][0],
            attrs=args[args_opt][1])

    # Check if it still could not find a section
    # if so use the Wikipedia API method and print this information to the user
    if ref_html == []:
        if main_html.find_all(["div", {"id": "copyvio"}]) != []:
            print("*This page contains a Copyright issue*")
            return []
        print(f"*Wiki format error or page stub* {page.title}")
        return page.links
    else:
        # get the first and only item in the list
        ref_html = ref_html[0]

    # remove everything in and below the references section
    main_str = str(main_html)
    references_str = str(ref_html)
    references_idex = main_str.find(references_str)
    page_content = main_str[:references_idex]

    # parse the new shortened HTML and get all links with a tile
    content_soup = BeautifulSoup(page_content, "html.parser")
    all_links = content_soup.find_all(
        name="a", attrs={"class": None, "title": re.compile(".")})
    all_links += content_soup.find_all(
        name="a", attrs={"class": "mw-disambig", "title": re.compile(".")})

    # Call get_titles to return only non-"Meta" Links
    return get_titles(all_links)


def get_titles(all_links):
    """
    Takes a BeutifulSoup ResultsSet of all links and returns only wanted links

    Args:
        all_links: (ResultsSet) A set of alll the links in the wikipedia article

    Returns a list of links without any "Meta" wiki links
    """
    links = set()
    meta_links = set()
    # for each link, Check if its a Meta page add it to a meta_links to remove
    for link in all_links:
        if re.search("^Edit section:", link["title"]):
            # This step is unnecessary but adds protection against errors
            meta_links.add(link["title"])
        elif re.search("^Wikipedia:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Help:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Talk:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Template:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^File:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Template talk:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Special:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Category:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^MediaWiki:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^About this Sound", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^#", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Portal:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^commons:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^Commons:", link["title"]):
            meta_links.add(link["title"])
        elif re.search("^ru:", link["title"]):
            meta_links.add(link["title"])
        # if the page is not a meta page add it to the set "links"
        else:
            links.add(link["title"])
    # Return the links that are not "Meta" pages
    return list(links - meta_links)


def get_min_path(paths):
    """
    Takes a list of paths and returns the shortest one.

    If there are more than one of the same length, returns the first one

    Args:
        Paths: (List) A set of all the paths between
            the starting page and the end page

    Returns a list of article titles in the shortest path
    """
    min_path = None
    min_len = 25
    # For each path check if it is shorter than the current min length
    # If so update the minimum length and path
    for path in paths:
        if len(path) < min_len:
            min_len = len(path)
            min_path = path
    return min_path


def plot_path(path):
    """
    Takes a found path and prints a formated version of the path

    Args:
        Path: (List) A set of all the links in the wikipedia article

    Returns a string verion of the path
    """
    if path == []:
        print("No path found, try more steps between pages!")
        return None
    path_str = "| "
    for page in path:
        path_str += page
        path_str += " ---> "
    path_str = path_str[:-5] + "|"
    # print(path_str)
    return path_str


def plot_all_paths(paths):
    """
    Takes a list of found paths and prints a formated version of the paths

    Args:
        Paths: (List) A set of all the paths between
            the starting page and the end page

    Returns a string verion of all the paths
    """
    formated = ""
    print(f"We found {len(paths)} links!")
    print(f"The shortest path(s) are {len(get_min_path(paths))} links long.")
    print(f"The first short path is: {plot_path(get_min_path(paths))}")
    print("\n-------------------------------\n")
    # If the list of pthats is empty, print out that result
    if paths == []:
        print("No paths found, try more steps between pages!")

    # Format each path and add it to a string to return
    # with newlines between paths
    for path in paths:            
        formated += plot_path(path) + "\n"
        print(plot_path(path))
    # Return a string containing all the paths
    return formated


def save_paths(paths, start, end, steps):
    """
    Takes a list of found paths and prints a formated version of the paths

    Saves the file with a title showing the start page, end page,
        and number of steps

    Args:
        Paths: (List) A set of all the paths between
            the starting page and the end page
        Start: (Str) The name of the page each path starts at
        End: (Str) The name of the page each path ends at
        Steps: (Int) The number of maximum steps between the start page and
            the end page

    Returns a string verion of all the paths
    """
    with open(f"paths/{start},_{end},_{steps}", "w") as f:
        print(f"We found {len(paths)} paths from {start} to {end}!", file=f)
        print(
            f"The shortest path(s) are {len(get_min_path(paths))} links long.",
            file=f)
        print(
            f"The first short path is: {plot_path(get_min_path(paths))}",
            file=f)
        print("\n-------------------------------\n", file=f)
        print("\n-------------------------------\n")
        print(plot_all_paths(paths), file=f)
