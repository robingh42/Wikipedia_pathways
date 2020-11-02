from helpers import *
# pathways_args = [start_page, end_page="Philosophy", *max_steps=20]

def disambiguation(pg_name, end_pg, max_len, trail, paths):
    trail.append(pg_name)
    if max_len <= 1:
        print(f"Nope not this: {trail}")
        return None
    for link in get_links(pg_name):
        if is_disamb(link):
            disambiguation(link, end_pg, max_len-1, trail[:], paths)
        elif is_page(link):
            get_pathway(get_page(link), end_pg, max_len-1, trail[:], paths)

def get_pathway(page, end_pg, max_len, trail, paths):
    trail.append(page.title)

    if has_end(page, end_pg):
        trail.append(end_pg.title)
        paths.append(trail)
        print(f"**Pathway {len(paths)}**: {trail}")
        return None
    elif max_len <= 1:
        print(f"Nope not this: {trail}")
        return None
    else:
        for link in get_links(page.title):
            if link not in trail:
                if is_disamb(link):
                    disambiguation(link, end_pg, max_len-1, trail[:], paths)
                elif is_page(link):
                    get_pathway(get_page(link), end_pg, max_len-1, trail[:], paths)

def get_all_pathways(start_page, end_page="Philosophy", max_steps=20):
    pass

def plot_path(path):
    pass

def get_min_path(paths):
    min_path = None
    min_len = 25
    for path in paths:
        if len(path) < min_len:
            min_len = len(path)
            min_path = path
    return min_path


def find_paths(start, end="Philosophy", max_links=2):
    trail = []
    paths = []

    start_pg = get_page(start)
    end_pg = get_page(end)

    get_pathway(start_pg, end_pg, max_links, trail, paths)

    return paths

