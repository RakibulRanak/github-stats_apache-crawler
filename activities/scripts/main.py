from dotenv import load_dotenv
import requests
import json
from tqdm import tqdm
from utils import Repository, RepostioyStats
from config import BASE_URL, BEARER_TOKEN


load_dotenv('../../.env')


def main():
    USER = input('Enter github username: ')

    response = requests.get(
        f'{BASE_URL}/users/{USER}/repos',
        headers={
            'Authorization': f'Bearer {BEARER_TOKEN}'
        }
    )
    repositories = response.json()
    print(f'Total public repositories found : {len(repositories)}')


    repo_metrics = []
    for repo in tqdm(repositories, desc='Fetching repository metrics'):
        repo_metrics.append(Repository(repo['name'], repo['stargazers_count'], repo['forks_count'], USER).to_dict())


    repo_stats = RepostioyStats(repo_metrics, USER)
    repo_stats.to_dict()


    final_stats_summary = {
        'user' : repo_stats.user,
        'stats' : repo_stats.to_dict(),
    }

    final_stats_detailed = {
        'user' : repo_stats.user,
        'stats' : repo_stats.to_dict(),
        'repositories' : repo_stats.repositories
    }

    with open('repo_stats_summary.json', 'w') as f:
        json.dump(final_stats_summary, f)

    with open('repo_stats_detailed.json', 'w') as f:
        json.dump(final_stats_detailed, f)

if __name__ == "__main__":
    main()