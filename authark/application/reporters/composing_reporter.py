from abc import ABC, abstractmethod
from authark.application.repositories import (
    UserRepository, DominionRepository, RoleRepository, RankingRepository,
    ResourceRepository, PolicyRepository,  PermissionRepository)
from .types import (
    QueryDomain, UserDictList, DominionDictList, RoleDictList,
    ExtendedRankingDictList, ExtendedDictList)


class ComposingReporter(ABC):

    @abstractmethod
    def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        """List user roles, resolving model references"""

    @abstractmethod
    def list_resource_policies(self, resource_id: str) -> ExtendedDictList:
        """List resource policies, resolving model references"""


class StandardComposingReporter(ComposingReporter):

    def __init__(self,
                 dominion_repository: DominionRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 resource_repository: ResourceRepository,
                 policy_repository: PolicyRepository,
                 permission_repository: PermissionRepository) -> None:
        self.dominion_repository = dominion_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.resource_repository = resource_repository
        self.permission_repository = permission_repository
        self.policy_repository = policy_repository

    def list_user_roles(self, user_id: str) -> ExtendedRankingDictList:
        rankings = self.ranking_repository.search(
            [('user_id', '=', user_id)])
        result = []
        for ranking in rankings:
            role = self.role_repository.get(ranking.role_id)
            dominion = self.dominion_repository.get(role.dominion_id)
            result.append({'ranking_id': ranking.id, 'role': role.name,
                           'dominion': dominion.name})

        return result

    def list_resource_policies(self, resource_id: str) -> ExtendedDictList:
        permissions = self.permission_repository.search(
            [('resource_id', '=', resource_id)])
        result = []
        for permission in permissions:
            policy = self.policy_repository.get(permission.policy_id)
            result.append({'permission_id': permission.id,
                           'policy': policy.name})

        return result
