import helpers as h


def get_pathway(page_name, end_pg, max_len, trail, paths):
    """
    Finds a list of all paths from a starting wikipedia page to an end page

    Assumes page_name is a valid wikipedia article title and end_pg is a valid
        Wikipedia Page Object

    Args:
        page_name: (Str) The name of the current article
        end_pg: (Wikipedia Page) The page the path should end at
        max_len: (Int) The number of maximum steps between the start page and
            the end page
        trail: (List) The current path being searched 
        Paths: (List) A set of all the paths between
            the starting page and the end page

    Returns nothing but appends a given list of paths
    """
    trail.append(page_name)  # add the current page to the current trail
    # Check if the page has the the end page as a link and
    # add it to thhe list of paths
    if h.has_end(page_name, end_pg):
        # if the page contains a link to the end page
        # add the end page to the trail, and add the trail to the paths list
        trail.append(end_pg.title)
        paths.append(trail)
        print(f"**Pathway {len(paths)}**: {h.plot_path(trail)}")
        return None
    # if the trail is above the maximum length return none
    elif max_len <= 1:
        print(f"Not a path: {trail}")
        return None
    
    else:
    # Check each of the links in the page
    # Continue branching looking for the end
        for link in h.get_links(page_name):
            if link not in trail:
                if h.is_page(link):
                    get_pathway(link, end_pg, max_len - 1, trail[:], paths)


def find_paths(start, end="Philosophy", max_links=3):
    """
    Takes a list of found paths and prints a formated version of the paths

    Saves the file with a title showing the start page, end page,
        and number of steps

    Args:
        Start: (Str) The name of the page each path starts at
        End: (Str) The name of the page each path ends at
        max_links: (Int) The number of maximum steps between the start page and
            the end page

    Returns a list of all the paths between the start page and end page.
    """
    trail = []  # Create a list to add the current trail to
    paths = []  # A set of all the paths between the start page and end page

    start_pg = h.get_page(start)  # Find a wiki page from the start page name
    end_pg = h.get_page(end)  # Find a wiki page from the end page name

    get_pathway(start_pg.title, end_pg, max_links, trail, paths)
    print("\n-------------------------------\n")
    # Save all the paths and print them
    h.save_paths(paths, start_pg.title, end_pg.title, max_links)
    return paths
