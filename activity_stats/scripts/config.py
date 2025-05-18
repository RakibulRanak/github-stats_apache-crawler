from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())

BEARER_TOKEN = os.getenv('GITHUB_TOKEN')
if BEARER_TOKEN :
    print('GITHUB TOKEN found in envirionment')
else:
    print('GITHUB TOKEN not found')
    raise Exception('GITHUB TOKEN not found')

BASE_URL = 'https://api.github.com/'