from abc import ABC, abstractmethod
from ..domain.repositories import (
    UserRepository, CredentialRepository,
    DominionRepository, RoleRepository,
    RuleRepository, PolicyRepository, RankingRepository)
from ..domain.common import QueryDomain, RecordList


class AutharkInformer(ABC):

    @abstractmethod
    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 0,
                     offset: int = 0) -> RecordList:
        """Returns a list of <<model>> dictionaries matching the domain"""

    @abstractmethod
    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        """Returns a the <<model>> records count"""


class StandardAutharkInformer(AutharkInformer):

    def __init__(self, user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 rule_repository: RuleRepository,
                 policy_repository: PolicyRepository,
                 ranking_repository: RankingRepository) -> None:
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.rule_repository = rule_repository
        self.policy_repository = policy_repository
        self.ranking_repository = ranking_repository

    async def search(self,
                     model: str,
                     domain: QueryDomain = None,
                     limit: int = 10000,
                     offset: int = 0) -> RecordList:
        repository = getattr(self, f'{model}_repository')
        return [vars(entity) for entity in
                await repository.search(
                domain or [], limit=limit, offset=offset)]

    async def count(self,
                    model: str,
                    domain: QueryDomain = None) -> int:
        repository = getattr(self, f'{model}_repository')
        return await repository.count(domain or [])