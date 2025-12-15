from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType


class GithubApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.github_api_url,
            content_type=ContentType.GITHUB_JSON,
            api_log_lvl=CFG.api_log_lvl,
        )

    def get_issue_state(self, issue_id: str) -> AssertableResponse:
        return self.get(
            url=f"/repos/{CFG.github_account_name}/{CFG.github_repo_name}/issues/{issue_id}",
            headers={
                "accept": ContentType.GITHUB_JSON.mime_type,
                "user-agent": CFG.github_token_name,
                "authorization": CFG.github_token,
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
