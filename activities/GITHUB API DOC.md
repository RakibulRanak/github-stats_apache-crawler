For our use case we need the user repositories. Then iterate over repository name and find the detailed metrics of that repository

Repositories of an user
https://api.github.com/repos/{user}/{repo}/

Now iterate over the array of response to get *name* of the repo, *stargazers_count*, *forks_count* (directly available)

And call the following api for the other metrics

commits_url = https://api.github.com/repos/{user}/{repo}/commits 

contributors_url = https://api.github.com/repos/{user}/{repo}/contributors

branches_url = https://api.github.com/repos/{user}/{repo}/branches{/branch} 

tags_url = https://api.github.com/repos/{user}/{repo}/tags

releases_url = https://api.github.com/repos/{user}/{repo}/releases

closed_issues_url = https://api.github.com/repos/{user}/{repo}/issues?state=closed 

environments_url = https://api.github.com/repos/{user}/{repo}/environments

None of the API provides metaData of the count, so we can simply get the lenght of the response. 


For details : https://docs.github.com/en/rest/

