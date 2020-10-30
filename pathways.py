import wikipedia as wiki
# pathways_args = [start_page, end_page="Philosophy", *max_steps=20]


def get_page(query):
    search = wiki.search(query)
    try:
        page = wiki.WikipediaPage(search[0])
    except wiki.exceptions.DisambiguationError as de:
        page = wiki.WikipediaPage(search[1])
    except wiki.exceptions.PageError as pe:
        return None
    return page


def is_disamb(page_name):
    try:
        page = wiki.WikipediaPage(page_name)
    except wiki.exceptions.DisambiguationError as de:
        return True
    except wiki.exceptions.PageError as pe:
        return False
    return False


def is_page(page_name):
    try:
        page = wiki.WikipediaPage(page_name)
    except wiki.exceptions.PageError as pe:
        return False
    return True


def get_links(page_name):
    # disambiguation
    try:
        return wiki.WikipediaPage(page_name).links
    except wiki.exceptions.DisambiguationError as de:
        return de.options
    pass


def has_end(page, end_page):
    return page.title == end_page.title


def disambiguation(pg_name, end_pg, max_len, trail, paths):
    disamb_trail = trail + [pg_name]
    for link in get_links(pg_name):
        if is_page(link):
            get_pathway(get_page(link), end_pg, max_len-1, disamb_trail, paths)

def get_pathway(page, end_pg, max_len, trail, paths):
    trail.append(page.title)

    if has_end(page, end_pg):
        paths.append(trail)
        print(f"**Pathway {len(paths)}**: {trail}")
        return None
    elif max_len <= 1:
        print(f"Nope not this: {trail}")
        return None
    else:
        pg_links = get_links(page.title)

        for link in get_links(page.title):
            if link not in trail:
                if is_disamb(link):
                    disambiguation(link, end_pg, max_len-1, trail, paths)
                elif is_page(link):
                    get_pathway(get_page(link), end_pg, max_len-1, trail[:], paths)
            else:
                pass

def get_all_pathways(start_page, end_page="Philosophy", max_steps=20):
    pass


def get_min_path(paths):
    min_path = None
    min_len = 25
    for path in paths:
        if len(path) < min_len:
            min_len = len(path)
            min_path = path
    return min_path


def plot_path(path):
    pass


def find_paths(start, end="Philosophy", max_links=3):
    
    trail = []
    paths = []

    start_pg = get_page(start)
    end_pg = get_page(end)

    get_pathway(start_pg, end_pg, max_links, trail, paths)

    return paths

