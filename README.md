# Wikipedia_pathways


## Importing the Wikipedia API

You will need to install the wikipedia package using the following command:
`pip install wikipedia`

Using this API might occasionaly cause a GuessedAtParserWarning as whomever
made it did not specify a parser. This is not a problem just might occasionaly
cause the program to print the error which does not affect the program at all.

If you want to prevent this, find wikipedia in your python librarys directory,
and `features="lxml"` as an argument into the BeautifulSoup call at `line 389`.
It will give you the path if the warning ever pops up.

## Finding the Paths Between Pages

This program is not a quick program to run, I reccomend that you don't go above 4 steps between pages. The code is constantly pulling from the internet or reading files, which can take a while as both of these are continualy branching to a set depth.

To actualy run the code:  
In your terminal run the command `python Six_Degrees_of_Wikipedia.py` and follow the prompts.  
Another wat is to import pathways.py and use `pathways.findpaths(args)`, where `args = start, end="Philosophy", max_links=3`.
