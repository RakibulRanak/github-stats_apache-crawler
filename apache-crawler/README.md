# Crawl over Apache Camel project and generate issue dataset

This project iterate over all issues of camel project from apache and generate datasets. If a specific issue number is given in program promt, it only fetch the specific issue.

From the issue these are the collected properties : 

`type, assignee, created_at, created_at_epoch, description, comments, id, url`

Comments consist of : 

`author, created_at, created_at_epoch, text`
# Instruction to run the project

- Install pip (if not already installed)

- Install the following libraries :
`pip install requests beautifulsoup4 selenium`

- run `python3 fetch-language.py`

- provide the issue id in prompt. If not given it will start fetching all issues.

- After the end of program, `camel_issue-{issue-no}.json` or `camel_issues-[{start}-{end}].json` will be created inside the current directoy. There will be `csv` file as well. But the representation of `json` is better.

- Additional : Executing all codeblocks of `crawler.ipynb` would do the same. Here we need to edit the variables, as there will be no prompt

# Information

Crawler takes approximate 8 minutes per 100 issues.
There are 22K+ issues, approximate time needed = ((22000 / 100) * 8) = 1760 minutes  ~ `30H`


# Basic overview of the workflow

Crawl over issue pages and scrap the properties. All properties can be scrapped using BeautifulSoup easily except comments. Comments are renderd using JS. Selenium is used to render the JS and extract comments.