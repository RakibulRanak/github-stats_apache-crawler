from config import BASE_URL, BEARER_TOKEN
import requests
import statistics


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

        self.stargazers_counts = [repo.get('stargazers_count', 0) for repo in repositories]
        self.forks_counts = [repo.get('forks_count', 0) for repo in repositories]
        self.commits_counts = [repo.get('commits_count', 0) for repo in repositories]
        self.contributors_counts = [repo.get('contributors_count', 0) for repo in repositories]
        self.branches_counts = [repo.get('branches_count', 0) for repo in repositories]
        self.tags_counts = [repo.get('tags_count', 0) for repo in repositories]
        self.releases_counts = [repo.get('releases_count', 0) for repo in repositories]
        self.closed_issues_counts = [repo.get('closed_issues_count', 0) for repo in repositories]
        self.environments_counts = [repo.get('environments_count', 0) for repo in repositories]
        

    def __get_median(self, counts):
        return statistics.median(counts) if counts else 0
    
    def __get_total(self, counts):
        return sum(counts)

    
    
    def to_dict(self):
        return {
            'total_repos': self.total_repos,
            'total_stargazers_count': self.__get_total(self.stargazers_counts),
            'median_stargazers_count': self.__get_median(self.stargazers_counts),
            'total_forks_count': self.__get_total(self.forks_counts),
            'median_forks_count': self.__get_median(self.forks_counts),
            'total_commits_count': self.__get_total(self.commits_counts),
            'median_commits_count': self.__get_median(self.commits_counts),
            'total_contributors_count': self.__get_total(self.contributors_counts),
            'median_contributors_count': self.__get_median(self.contributors_counts),
            'total_branches_count': self.__get_total(self.branches_counts),
            'median_branches_count': self.__get_median(self.branches_counts),
            'total_tags_count': self.__get_total(self.tags_counts),
            'median_tags_count': self.__get_median(self.tags_counts),
            'total_releases_count': self.__get_total(self.releases_counts),
            'median_releases_count': self.__get_median(self.releases_counts),
            'total_closed_issues_count': self.__get_median(self.closed_issues_counts),
            'median_issues_count': self.__get_median(self.closed_issues_counts),
            'total_environments_count' : self.__get_total(self.environments_counts),
            'median_environments_count' : self.__get_median(self.environments_counts) 
        }