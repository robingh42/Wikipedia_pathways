def get_min_path(paths):
    min_path = None
    min_len = 25
    for path in paths:
        if len(path) < min_len:
            min_len = len(path)
            min_path = path
    return min_path


def plot_path(path):
    if path == []:
        print("No path found, try more steps between pages!")
        return None
    path_str = "| "
    for page in path:
        path_str += page
        path_str += " ---> "
    path_str = path_str[:-5]+ "|"
    # print(path_str)
    return path_str


def plot_all_paths(paths):
    formated = ""
    print(f"We found {len(paths)} links!")
    if paths == []:
        print("No paths found, try more steps between pages!")
    for path in paths:
        if path == get_min_path(paths):
            formated += "Shortest Path: "
            print("Shortest Path: ", end = "")
        formated += plot_path(path) + "\n"
        print(plot_path(path))
    return formated
    

def save_paths(paths,start,end,steps):
    with open(f"paths/{start},_{end},_{steps}", "w") as f:
        print(f"We found {len(paths)} paths from {start} to {end}!", file=f)
        print("\n-------------------------------\n")
        print(plot_all_paths(paths), file=f)