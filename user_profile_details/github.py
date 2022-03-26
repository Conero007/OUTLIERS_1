import requests
from bs4 import BeautifulSoup


def fetch_github_data(username):
    url = f'https://api.github.com/users/{username}'
    response = requests.get(url).json()

    data_needed = ["company", "followers", "public_repos"]
    try:
        overall_data = {'SUCCESS': True}
        for field in data_needed:
            overall_data[field] = response[field]
        overall_data.update(fetch_repos_data(username))
        overall_data["total commits"] = fetch_commit_count(username)
    except:
        return {'SUCCESS': False}

    # ["company", "followers", "public_repos", "total commits"]
    return overall_data


def fetch_commit_count(username):
    url = "https://github.com/" + username
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    res = soup.find('div', class_='js-yearly-contributions').div.h2.text
    res = res.split('\n')[1].strip()

    return res


def fetch_repos_data(username):
    page_no = 1
    repo_data = []
    repos_url = f'https://api.github.com/users/{username}/repos'

    while True:
        url = repos_url + '?page=' + str(page_no)
        response = requests.get(url).json()
        repos_fetched = len(response)
        repo_data.extend(response)
        if repos_fetched != 30:
            break
        page_no = page_no + 1

    data_needed = ["watchers_count", "forks_count", "stargazers_count"]
    data = {field: 0 for field in data_needed + ["commits_count"]}

    for repo in repo_data:
        for field in data_needed:
            data[field] += int(repo[field])

    return data