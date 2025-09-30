import io
import sys
import requests
import pytest

def main():
    github_api("richkempinski") # Provided example repository
    # github_api("Cold-Change") # My repository

def github_api(username):
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Now 'data' contains the JSON response as a Python object
        print("-" * 45)
        for repo in data:
            commits_url = repo['commits_url'][:-6]
            commits_response = requests.get(commits_url)
            commits_data = commits_response.json()
            name = repo['name']
            commits = len(commits_data)
            print(f"Repo: {name}   Commits: {commits}")
            print("-" * 45)
    else:
        print(f"Failed to retrieve data.")

def test_github_api(capsys):
    # test valid user
    github_api("richkempinski")
    captured = capsys.readouterr().out

    # Assertions
    assert isinstance(captured, str)
    assert "Repo:" in captured
    assert "Commits:" in captured
    assert len(captured) > 0

    # test invalid user
    github_api("this_user_should_not_exist_123456")
    captured = capsys.readouterr().out.strip()

    # Assertions
    assert captured == "Failed to retrieve data."
    assert captured is not None
    assert isinstance(captured, str)

if __name__ == "__main__":
    main()