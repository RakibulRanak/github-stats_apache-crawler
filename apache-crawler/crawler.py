import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from selenium import webdriver

DEFAULT_APACHE_PROJECT_URL = 'https://issues.apache.org/jira/browse/CAMEL'

ISSUE_NO_START = 1
ISSUE_NO_END = 22079

SPECIFIC_ISSUE_NO = input("Enter the issue number (press Enter to crawl all): ")
if SPECIFIC_ISSUE_NO.strip():
    try:
        SPECIFIC_ISSUE_NO = int(SPECIFIC_ISSUE_NO)
        if 1 <= SPECIFIC_ISSUE_NO <= 22079:
            ISSUE_NO_START = SPECIFIC_ISSUE_NO
            ISSUE_NO_END = SPECIFIC_ISSUE_NO
        else:
            print("Please enter a number between 1 and 22079")
            exit(1)
    except ValueError:
        print("Please enter a valid number")
        exit(1)

def time_epoch(date):
    dt = datetime.strptime(date, "%d/%b/%y %H:%M").replace(tzinfo=timezone.utc)
    epoch = int(dt.timestamp())
    return epoch

def fetch_issue_body(issue_url):
    res = requests.get(issue_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    type_tag = soup.find('span', {'id': 'type-val', 'class': 'value'})
    type = type_tag.text.strip() if type_tag else None

    assignee_tag = soup.find('span', {'class':'user-hover'})
    assignee = assignee_tag.text.strip() if assignee_tag else None

    created_tag = soup.find('span', {'id': 'created-val', 'data-fieldtype': 'datetime'})
    created_at = created_tag.text.strip() if created_tag else None

    created_at_epoch = time_epoch(created_at) if created_at else None

    desc_tag = soup.find('div', {'id':'description-val'})
    description = desc_tag.get_text(strip=True) if desc_tag else None

    return {
        'type' : type,
        'assignee' : assignee,
        'createdAt' : created_at,
        'created_at_epoch' : created_at_epoch,
        'description' : description
    }

def fetch_issue_comments(issue_url):
    driver = webdriver.Chrome()
    driver.get(issue_url)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')

    comments_sec = soup.find_all('div', {'class':'issue-data-block activity-comment twixi-block expanded'})
    comments = []

    for sec in comments_sec:
        comment_sec = sec.find('div', {'class':'twixi-wrap verbose actionContainer'})
        
        author_tag = comment_sec.find('a', {'class' : 'user-hover user-avatar'})
        author = author_tag.text.strip() if author_tag else None

        time_tag = comment_sec.find('time')
        created_at = time_tag.text.strip() if time_tag else None
        created_at_epoch = time_epoch(created_at) if created_at else None

        body_tag = comment_sec.find('div', {'class':'action-body flooded'})
        text = body_tag.get_text(strip=True) if body_tag else None

        comment = {
            "author" : author,
            "created_at":created_at,
            "created_at_epoch":created_at_epoch,
            "text": text
        }
        comments.append(comment)
    return comments

issue_no = ISSUE_NO_START
issues = []

while issue_no <= ISSUE_NO_END:
    issue_url = f'{DEFAULT_APACHE_PROJECT_URL}-{issue_no}'
    try:
        issue = fetch_issue_body(issue_url)
        comments = fetch_issue_comments(issue_url)
        issue['comments'] = comments
        issue['id'] = issue_no
        issue['url'] = issue_url
        issues.append(issue)
        print(f"issue done: {issue_no}")
    except Exception as e:
        print(f"Error in issue {issue_no}: {e}")
    issue_no +=1

import json

with open('camel_issues.json', 'w', encoding='utf-8') as f:
    json.dump(issues, f, indent=2, ensure_ascii=False)
print(f"camel_issues.json created successfully")

import csv
import json

fieldnames = list(issues[0].keys()) 

with open('camel_issues.csv', 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for issue in issues:
        row = issue.copy() 
        row['comments'] = json.dumps(row['comments'], ensure_ascii=False)
        writer.writerow(row)
print(f"camel_issues.csv created successfully")