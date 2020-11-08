# Wikipedia_pathways

In the Wikipedia game the goal is to get from one Wikipedia page to another in the shortest amount of clicks. You can only use the links in the main article. `Talk:` pages and other meta Wikipedia pages are un interesting and outside of the heart of the game.

This project is a deviation of this game. Its goal is to find all the valid pathways between the two wikipedia pages.

It produces pathway results as a list, or as a formated string:
| Toothpaste ---> Apricot ---> Alexander the Great | 


## Importing the Wikipedia API

You will need to install the wikipedia package using the following command:
`pip install wikipedia`

Using this API might occasionaly cause a GuessedAtParserWarning as whomever
made it did not specify a parser. This is not a problem just might occasionaly
cause the program to print the error which does not affect the program at all.

If you want to prevent this, find wikipedia in your python librarys directory,
and `features="lxml"` as an argument into the BeautifulSoup call at `line 389`.
It will give you the path if the warning ever pops up.

## Directories

If you pull the whole project you should already have all the nessisary directorys. Otherwise for this code to run properly you should have the directories `/link_data` and `/paths` in the same directory as `pathways.py`, `helpers.py`, and `Six_Degrees_of_Wiki.py`.



## Finding the Paths Between Pages

This program is not a quick program to run, I reccomend that you don't go above 4 steps between pages. The code is constantly pulling from the internet or reading files, which can take a while as both of these are continualy branching to a set depth.

To actualy run the code:  
In your terminal run the command `python Six_Degrees_of_Wikipedia.py` and follow the prompts.  
Another way is to import pathways.py and use `pathways.find_paths(start, end="Philosophy", max_links=3`)`

If you only want a list of paths and not a formated string use the function `get_pathway(page_name, end_pg, max_len, trail, paths):`  
Make sure to give this function:  
- page_name: the name of an existing page  
- end_pg: a Wikipedia Page object such as one created by `helpers.get_page()` or `wikipedia.page()`  
- max_len: an int specifying the max depth to search  
- trail: give this a empty list that it can modify  
- paths: a list to add paths to  
Check `pathways.find_paths()` if you need an example of this
