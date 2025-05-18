import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import subprocess
from tqdm import tqdm
from selenium import webdriver
import json
import statistics
import time

USER = input("Enter github username: ")
org_input = input("Is the user an organization? (yes / no): ")
IS_ORG = org_input.lower() == 'yes'

BASE_URL = 'https://github.com'

def get_repo_names(page, user, is_org = False):
    url = f'{BASE_URL}/orgs/{user}/repositories?page={page}' if is_org else f'{BASE_URL}/{user}?tab=repositories&page={page}'
    repo_names = []

    if is_org:
        driver = webdriver.Chrome()
        driver.get(url)
        time.sleep(0.5)
        html = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html, 'html.parser')
        repo_elements = soup.find_all('h4', class_=lambda c: c and 'Title-module__heading') 

        for element in repo_elements:
            name_tag = element.find('a')
            name = name_tag.text.strip() if name_tag else None
            if name:
                repo_names.append(name)
    else :
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        repo_elements = soup.find_all('h3', {'class': 'wb-break-all'})
        for element in repo_elements:
            name_tag = element.find('a')
            name = name_tag.text.strip() if name_tag else None
            if name:
                repo_names.append(name)
    return repo_names



repo_urls = []
repo_names = []
page = 1
while True:
    names = get_repo_names(page, USER, IS_ORG)
    if len(names) == 0:
        break
    repo_names.extend(names)
    for name in names:
        repo_url = f'{BASE_URL}/{USER}/{name}'
        repo_urls.append(repo_url)
    page +=1
    
print(f'Total repositories to clone : {len(repo_names)}')

dir_path = f'clones/{USER}'
os.makedirs(dir_path, exist_ok=True)

df = pd.DataFrame({
    'name' : repo_names,
    'url' : repo_urls
})
df.to_csv(f'{dir_path}/{USER}_urls.csv', index=False)

for url in tqdm(repo_urls):
    subprocess.run(['git', 'clone', url], cwd=dir_path)

languages = ["Python","JavaScript","Java","TypeScript","C#","C++","Go","PHP","Ruby","Bourne Shell"]

path = f'clones/{USER}'
lang_stats = {}

for lang in languages:
    lang_stats[lang] = []

for repo in repo_names:
    repo_path = os.path.join(path, repo)

    result = subprocess.run(
        ["cloc", repo_path, f"--include-lang={','.join(languages)}", "--json"],
        capture_output=True,
        text=True
    )

    data = json.loads(result.stdout)
    repo_summary = {"repo_name": repo, "total": 0}

    for lang in languages:
        count = data.get(lang, {}).get("code", 0)
        lang_stats[lang].append(count)

total_summary = {}
for lang in languages:
    lang_counts = lang_stats[lang]
    print(lang, lang_counts)
    total = sum(lang_counts)
    median = statistics.median(lang_counts) if lang_counts else 0
    total_summary[lang] = {
        "total" : total,
        "median" : median
    }

with open(f'{os.path.dirname(__file__)}/{USER}_language_summary.json', 'w') as f:
    json.dump(total_summary, f)

print(f'{USER}_language_summary.json created successfully' )