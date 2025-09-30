import io
import sys
import requests
import pytest
from unittest.mock import patch, MagicMock
from testing_github_api import github_api


def test_github_api_mock(capsys):
    # Mock repo response
    mock_repo_response = MagicMock()
    mock_repo_response.status_code = 200
    mock_repo_response.json.return_value = [
        {"name": "repo1", "commits_url": "https://api.github.com/repos/test/repo1/commits{/sha}"},
        {"name": "repo2", "commits_url": "https://api.github.com/repos/test/repo2/commits{/sha}"}
    ]

    # Mock commits responses
    mock_commit_response1 = MagicMock()
    mock_commit_response1.json.return_value = [{"sha": "1"}, {"sha": "2"}]  # 2 commits
    mock_commit_response2 = MagicMock()
    mock_commit_response2.json.return_value = [{"sha": "a"}]  # 1 commit

    # Patch requests.get so it returns our mock responses in order
    with patch("requests.get", side_effect=[mock_repo_response, mock_commit_response1, mock_commit_response2]):
        github_api("testuser")
        captured = capsys.readouterr().out

    # Assertions
    assert isinstance(captured, str)
    assert "Repo: repo1   Commits: 2" in captured
    assert "Repo: repo2   Commits: 1" in captured
    assert "-" * 45 in captured
    assert len(captured) > 0