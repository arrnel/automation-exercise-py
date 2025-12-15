from http import HTTPStatus
from typing import Union

from src.client.core.condition.conditions import Conditions
from src.client.github_api_client import GithubApiClient
from src.model.enum.github_issue_type import IssueType


class GithubApiService:

    def __init__(self):
        self.github_client = GithubApiClient()

    def get_issue_state(self, issue_number: Union[int, str]) -> IssueType:
        issue_type = (
            self.github_client.get_issue_state(issue_number)
            .check(Conditions.status_code(HTTPStatus.OK))
            .extract()
            .as_value("state")
        )
        return IssueType(issue_type)
