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

None of the API provides metaData of the count. We iterate over the paginatated api untill there is no data and increment the count. 

Btw, there is an efficient way to do this. Response provide a Link header with the last page link. We could extract the page number from the header with a regex. And directly visit the last page to get the count of response of the last page. For all the other page, we could simply sum up as `count += (total page - 1) * page size` without visiting. 


For details : https://docs.github.com/en/rest/

