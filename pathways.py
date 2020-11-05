from helpers import get_links, get_page, is_page, is_disamb, has_end
from file_management import save_paths, plot_path

def disambiguation(pg_name, end_pg, max_len, trail, paths):
    trail.append(pg_name)
    if max_len <= 1:
        print(f"Not a path: {trail}")
        return None
    for link in get_links(pg_name):
        if is_disamb(link):
            disambiguation(link, end_pg, max_len-1, trail[:], paths)
        elif is_page(link):
            get_pathway(get_page(link), end_pg, max_len-1, trail[:], paths)

def get_pathway(page_title, end_pg, max_len, trail, paths):
    trail.append(page_title)

    if has_end(page_title, end_pg):
        trail.append(end_pg.title)
        paths.append(trail)
        print(f"**Pathway {len(paths)}**: {plot_path(trail)}")
        return None
    elif max_len <= 1:
        print(f"Not a path: {trail}")
        return None
    else:
        for link in get_links(page_title):
            if link not in trail:
                if is_disamb(link):
                    disambiguation(link, end_pg, max_len-1, trail[:], paths)
                elif is_page(link):
                    get_pathway(link, end_pg, max_len-1, trail[:], paths)


def find_paths(start, end="Philosophy", max_links=3):
    trail = []
    paths = []

    start_pg = get_page(start)
    end_pg = get_page(end)

    get_pathway(start_pg.title, end_pg, max_links, trail, paths)
    print("\n-------------------------------\n")
    # plot_all_path(paths)
    save_paths(paths,start_pg.title,end_pg.title,max_links)
    return paths
