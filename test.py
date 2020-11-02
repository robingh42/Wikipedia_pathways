import helpers

for i in helpers.get_links("France"):
    print(i)
    print(len(helpers.get_links(i)))
    