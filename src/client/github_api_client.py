from src.client.core.assertion import AssertableResponse
from src.client.core.base_api_client import RestClient
from src.config.config import CFG
from src.model.enum.meta.content_type import ContentType
from src.model.enum.meta.log_level import ApiLogLvl


class GithubApiClient(RestClient):

    def __init__(self):
        super().__init__(
            base_url=CFG.github_api_url,
            content_type=ContentType.GITHUB_JSON,
            api_log_lvl=ApiLogLvl.NONE,
            user_agent=CFG.github_token_name,
        )

    def get_issue_state(self, issue_id: str) -> AssertableResponse:
        return self.get(
            url=f"/repos/{CFG.github_account_name}/{CFG.github_repo_name}/issues/{issue_id}",
            headers={
                "accept": ContentType.GITHUB_JSON.mime_type,
                # "accept-encoding": None,
                # "connection": None,
                "user-agent": CFG.github_token_name,
                "authorization": f"Bearer {CFG.github_token}",
                "X-GitHub-Api-Version": "2022-11-28",
            },
        )
