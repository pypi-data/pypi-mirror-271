"""
Integration Issue
"""

from abc import ABC, abstractmethod

from regscale.models import Issue


class IntegrationIssue(ABC):
    """
    Abstract class for Integration Issue
    """

    def __init__(
        self,
        **kwargs,
    ):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @abstractmethod
    def pull(self):
        """
        Pull inventory from an Integration platform into RegScale
        """

    def create_issues(
        self,
        issues: list[Issue],
    ):
        """
        Create issues in RegScale

        :param list[Issue] issues: list of issues to create
        """
        Issue.batch_create(items=issues)
