from pathways import find_paths
max_links = ""

print("\n\n\nWelcome to *Six Degrees of Wikipedia*")
print("Our goal is to find the links inbetween two pages on Wikipedia.")
print("As the search runs, files will be saved localy to speed up later runs.")
print("This might take some time to run initialy, sorry.")

print("\n-------------------------------\n")

print("What page would you like to start at: ")
page = input()

print("The default end is Philosophy and the max chain links is 3")
print("Would you like to change this? (y/n)")
check_defaults = input()

if check_defaults[0].lower() == "y":
    print("What page would you like to end at: ")
    end_page = input()
    while not max_links.isdigit():
        print("How many links between articles do you want: ")
        max_links = input()
    link_num = int(max_links)
    print("\n-------------------------------\n")
    find_paths(page, end=end_page, max_links=link_num)
else:
    find_paths(page)
