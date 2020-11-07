from pathways import find_paths
"""
This script is used to provide an easy experiance for the user to run
    find_paths() and find the paths between two wikipedia pages.

Args:
    User inupt:
        Page: (Str) The starting page for find_paths() search
        check_defaults: (Str) If the first character is "y", this determines
            if find_paths should use the defaults or not
        end_page: (Str) The page name find_paths is searching for
        max_links: (Str) Should be an integer, changes the maximum search
            depth of find_paths

Returns a file containing all the paths between th start page and the end page
"""
max_links = ""

print("\n\n\nWelcome to *Six Degrees of Wikipedia*")
print("Our goal is to find the links inbetween two pages on Wikipedia.")
print("As the search runs, files will be saved localy to speed up later runs.")
print("This might take some time to run initialy, sorry.")

print("\n-------------------------------\n")
# Prompt the user for the starting wikipedia page
page = input("\tWhat page would you like to start at: ")
# Ask the user if they would like to use default search arguments
print("\nThe default end is Philosophy and the maximum number of chains is 3")
check_defaults = input("\n\tWould you like to keep this? (y/n): ")
# If the user answers anything starting with "y", use the daufault agrs
# otherwise ask for the ending page and maximum depth
if check_defaults[0].lower() != "y":
    end_page = input("\n\tWhat page would you like to end at: ")
    while not max_links.isdigit():
        max_links = input("\n\tHow many links between articles do you want: ")
    link_num = int(max_links)
    print("\n-------------------------------\n")
    # Search for all pathways using custom search
    find_paths(page, end=end_page, max_links=link_num)
else:
    print("\n-------------------------------\n")
    # Search for all pathways using default search
    find_paths(page)
