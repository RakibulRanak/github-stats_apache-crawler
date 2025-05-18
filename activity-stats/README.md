# Generate activity statistics from all the github repositories of an user. 

The stats includes - Total and median number of commits, stars, contributors, branches, tags, forks, releases, closed issues, and environments. Github API is used to perform this task. 

## Instruction to run the project

- Install pip (if not already installed)
- Install the following libraries : 
`pip install python-dotenv requests tqdm`
- Create a `.env` file at the root of the repository. Create your github api token and set variable `GITHUB_TOKEN` in `.env`
- Run `python3 scripts/main.py`
- Provide the `username` of the github in prompt
- After the end of program, you will find 2 files under scripts folder as following :
    `{username}_activity_detailed.json` and `{username}_activity_summary.json`
- Additional : Executing all codeblocks of `fetch-activities.ipynb` would do the same. Here we need to edit the variables, as there will be no prompt


## Basic overview of the workflow
For our use case we need to fetch all repositories of an User. Then iterate over repository and find the detailed metrics of that repository.

### Repositories of an user
https://api.github.com/repos/{user}/{repo}/

Now iterate over the array of response to get *name* of the repo, *stargazers_count*, *forks_count* (directly available)

And call the following api for the other metrics

commits = https://api.github.com/repos/{user}/{repo}/commits 

contributors = https://api.github.com/repos/{user}/{repo}/contributors

branches = https://api.github.com/repos/{user}/{repo}/branches{/branch} 

tags = https://api.github.com/repos/{user}/{repo}/tags

releases = https://api.github.com/repos/{user}/{repo}/releases

closed_issues = https://api.github.com/repos/{user}/{repo}/issues?state=closed 

environments = https://api.github.com/repos/{user}/{repo}/environments

None of the API provides metaData of the count. We iterate over the paginatated api untill there is no data and increment the count. 

Btw, there is an efficient way to do this. Response provide a Link header with the last page link. We could extract the page number from the header with a regex. And directly visit the last page to get the count of response of the last page. For all the other page, we could simply sum up as `count += (total page - 1) * page size` without visiting. But for the issues API, we are unable to skip pages like that. GitHub’s Issues API returns both issues and pull requests. Only way to filter out the pull requests from the actual issues is to go through every  item in the response and discard it if it contains `pull_request` object inside it. 


For details : https://docs.github.com/en/rest/

