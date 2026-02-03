from typing import Optional


def disabled_by_issue(issue_id: int, reason: Optional[str] = None):
    if reason is None:
        reason = f"Disabled by issue: {issue_id}"

    def decorator(func):
        func.__disabled_by_issue__ = {
            "issue_id": issue_id,
            "reason": reason,
        }
        return func

    return decorator
