import helpers

#for i in helpers.get_links("France"):
    #print(i)
    #print(len(helpers.get_links(i)))

def read_links(title):
    with open(f"link_data/{title}", "r") as f:
        read_data = f.read()
        return read_data.split("\n")[:-1]

def save_links(title, links):
    with open(f"link_data/{title}", "w") as f:
        for link in links:
            f.write(link + "\n")
        return True

test_now = ['Blue Heelers', 'IMDb', 'Neighbours']
test_now2 = {'Blue Heelers', 'IMDb', 'Neighbours'}

save_links("Zoe Stark",test_now2)

print(read_links("Zoe Stark"))
    