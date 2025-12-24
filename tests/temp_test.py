from typing import Optional

from src.model.enum.github_issue_type import IssueType
from src.service.github_api_service import GithubApiService
from src.util.decorator.step_logger import step_log


def test_github():
    print(github_step())


@step_log.log("Github step")
def github_step() -> Optional[IssueType]:
    return GithubApiService().get_issue_state(1)
