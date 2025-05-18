# Genereate programming language statistics from all github repositories of an user or organization

The stats includes - total and median number of source code lines per programming languages used from all the repositories of an user/org.


# Instruction to run the project

- Install pip (if not already installed)

- Install the following libraries :
`pip install beautifulsoup4 selenium requests pandas tqdm`

- Install `cloc` locally. This package is used to count lines of code in repositories. Find official instructions here : https://github.com/AlDanial/cloc#installing-cloc

- run `python3 fetch-language.py`

- provide the information while asked in prompt

- After the end of program, `{username}_language_summary.json` will be created inside the current directoy with the statistics.

- Additional : Executing all codeblocks of `fetch-languages.ipynb` would do the same. Here we need to edit the variables, as there will be no prompt 

## Language supports

Currently, Supported languages are :

`["Python","JavaScript","Java","TypeScript","C#","C++","Go","PHP","Ruby","Bourne Shell"]` 

This list can be modified in the code to add support for more languages


## Basic overview of the workflow

We need to clone all repositories locally and run cloc iteratively to get the code/line counts. 

To fetch repositories of an user/org, the easy way is to use github api. But in this proeject, web-scrapping is used. For fetching the repositories of a regular user, BeautifulSoup is sufficient as the html exposes every details. But for the organization user, repositories view is a bit different. The repositories are not preloaded in html, it gets loaded later using JS rendering. Selenium is used in this case to execute the JS to return the html of organization repositories.

After all repositoy names are collected, repositories were cloned via `git clone {repo}`. Then cloc is iteratively applied to individual repositories to  generate programming language line counts. These counts are stored in data structure to finally aggregate and calculate the sum and median. 
