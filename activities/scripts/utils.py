from config import BASE_URL, BEARER_TOKEN
import requests


class Repository:
    user = ''
    name = ''
    stargazers_count = 0
    forks_count = 0
    
    # further api metrics

    commits_count = 0
    contributors_count = 0
    branches_count = 0
    tags_count = 0
    releases_count = 0
    closed_issues_count = 0
    enviroments_count = 0

    def __init__(self, name, stargazers_count, forks_count, user):
        self.user = user
        self.name = name
        self.stargazers_count = stargazers_count
        self.forks_count = forks_count

        self.commits_count = self.__get_metrics_count('commits')
        self.contributors_count = self.__get_metrics_count('contributors')
        self.branches_count = self.__get_metrics_count('branches')
        self.tags_count = self.__get_metrics_count('tags')
        self.closed_issues_count = self.__get_metrics_count('issues')
        self.releases_count = self.__get_metrics_count('releases')    
        self.enviroments_count = self.__get_metrics_count('environments')    
  

    def __get_metrics_count(self, url_extension):
        total_count = 0
        page = 1
        per_page = 100  # Maximum allowed by GitHub API
        
        while True:
            url = f'{BASE_URL}/repos/{self.user}/{self.name}/{url_extension}?per_page={per_page}&page={page}'
            if url_extension == 'issues':
                url = f'{url}&state=closed'
                
            response = requests.get(url, headers={
                'Authorization': f'Bearer {BEARER_TOKEN}'
            })
            
            if url_extension == 'environments':
                return response.json().get('total_count', 0)
                
            data = response.json()
            
            if not data:  # Empty response means we've reached the end
                break
            
            if url_extension == 'issues':
                issues_without_pull_request = 0
                for issue in data:
                    if not issue.get('pull_request'):  # If pull_request is None, it's a regular issue
                        issues_without_pull_request += 1
                total_count += issues_without_pull_request
            else:
                total_count += len(data)
                
            page += 1
            
        return total_count
    
    def to_dict(self):
        return {
            'name': self.name,
            'stargazers_count': self.stargazers_count,
            'forks_count': self.forks_count,
            'commits_count': self.commits_count,
            'contributors_count': self.contributors_count,
            'branches_count': self.branches_count,
            'tags_count': self.tags_count,
            'releases_count': self.releases_count,
            'closed_issues_count': self.closed_issues_count,
            'environments_count' : self.enviroments_count
            
        }



class RepostioyStats:
    
    def __init__(self, repositories, user):
        self.repositories = repositories
        self.total_repos = len(repositories)
        self.user = user

        self.total_stargazers_count = sum([repo.get('stargazers_count') for repo in repositories])
        self.median_stargazers_count = self.__get_median(self.total_stargazers_count)
        
        self.total_forks_count = sum([repo.get('forks_count') for repo in repositories])
        self.median_forks_count = self.__get_median(self.total_forks_count)
        
        self.total_commits_count = sum([repo.get('commits_count') for repo in repositories])
        self.median_commits_count = self.__get_median(self.total_commits_count)

        self.total_contributors_count = sum([repo.get('contributors_count') for repo in repositories])
        self.median_contributors_count = self.__get_median(self.total_contributors_count)

        self.total_branches_count = sum([repo.get('branches_count') for repo in repositories])
        self.median_branches_count = self.__get_median(self.total_branches_count)

        self.total_tags_count = sum([repo.get('tags_count') for repo in repositories])
        self.median_tags_count = self.__get_median(self.total_tags_count)

        self.total_releases_count = sum([repo.get('releases_count') for repo in repositories])
        self.median_releases_count = self.__get_median(self.total_releases_count)

        self.total_closed_issues_count = sum([repo.get('closed_issues_count') for repo in repositories])
        self.median_closed_issues_count = self.__get_median(self.total_closed_issues_count)
        
        self.total_enviroments_count = sum([repo.get('environments_count') for repo in repositories])
        self.median_enviroments_count = self.__get_median(self.total_enviroments_count)
    

    def __get_median(self, value):
        return round(value / self.total_repos, 2)
    
    def to_dict(self):
        return {
            'total_repos': self.total_repos,
            'total_stargazers_count': self.total_stargazers_count,
            'median_stargazers_count': self.median_stargazers_count,
            'total_forks_count': self.total_forks_count,
            'median_forks_count': self.median_forks_count,
            'total_commits_count': self.total_commits_count,
            'median_commits_count': self.median_commits_count,
            'total_contributors_count': self.total_contributors_count,
            'median_contributors_count': self.median_contributors_count,
            'total_branches_count': self.total_branches_count,
            'median_branches_count': self.median_branches_count,
            'total_tags_count': self.total_tags_count,
            'median_tags_count': self.median_tags_count,
            'total_releases_count': self.total_releases_count,
            'median_releases_count': self.median_releases_count,
            'total_closed_issues_count': self.total_closed_issues_count,
            'median_issues_count': self.median_closed_issues_count,
            'total_environments_count' : self.total_enviroments_count,
            'median_environments_count' : self.median_enviroments_count 
        }