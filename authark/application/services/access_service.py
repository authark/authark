import json
from typing import Dict, Any, List
from abc import ABC, abstractmethod
from ..models import User, Token, Role
from ..repositories import (
    RankingRepository, RoleRepository, DominionRepository,
    ResourceRepository)
from ..services import AccessTokenService


class AccessService(ABC):
    @abstractmethod
    def generate_token(self, user: User) -> Token:
        "Generate payload method to be implemented."


class StandardAccessService(AccessService):

    def __init__(self, ranking_repository: RankingRepository,
                 role_repository: RoleRepository,
                 dominion_repository: DominionRepository,
                 grant_repository: GrantRepository,
                 resource_repository: ResourceRepository,
                 permission_repository: PermissionRepository,
                 policy_repository: PolicyRepository,
                 token_service: AccessTokenService) -> None:
        self.ranking_repository = ranking_repository
        self.role_repository = role_repository
        self.dominion_repository = dominion_repository
        self.resource_repository = resource_repository
        self.grant_repository = grant_repository
        self.permission_repository = permission_repository
        self.policy_repository = policy_repository
        self.token_service = token_service

    def generate_token(self, user: User) -> Token:
        access_payload = self._build_payload(user)
        access_token = self.token_service.generate_token(access_payload)

        return access_token

    def _build_payload(self, user: User) -> Dict[str, Any]:
        payload = self._build_basic_info(user)
        payload['authorization'] = self._build_authorization(user)
        return payload

    def _build_basic_info(self, user: User) -> Dict[str, Any]:
        return {
            'sub': user.id,
            'email': user.email,
            'name': user.name,
            'gender': user.gender,
            'attributes': user.attributes
        }

    def _build_authorization(self, user: User) -> Dict[str, Any]:
        authorization = {}  # type: Dict[str, Any]
        rankings = self.ranking_repository.search([('user_id', '=', user.id)])
        roles = self.role_repository.search([('id', 'in', [
            ranking.role_id for ranking in rankings])])
        dominions = self.dominion_repository.search([('id', 'in', [
            role.dominion_id for role in roles])])

        for dominion in dominions:
            roles = [role.name for role in roles
                     if role.dominion_id == dominion.id]
            permissions = self._build_permissions(roles)
            authorization[dominion.name] = {
                "roles":  roles,
                "permissions": permissions
            }

        return authorization

    def _build_permissions(self, dominion: Dominion,
                           roles: List[Role]) -> Dict[str, Any]:
        permissions = []
        for role in roles:
            permission_ids = [
                grant.permission_id for grant in self.grant_repository.search(
                    [('role_id', '=', role.id)])]
            permissions.extend(self.permission_repository.search(
                [('id', 'in', permission_ids)]))

        resources_dict = {
            resource.id: resource.name
            for resource in self.resource_repository.search(
                [('dominion_id', '=', dominion.id)])}

        permissions_dict = {}
        for permission in permissions:
            resource_name = resources_dict[permission.resource_id]
            policy_dict = vars(self.policy_repository.search(
                [('id', '=', permission.policy_id)])[0])
            del policy_dict['id']

            permissions_dict[resource_name] = (
                permissions_dict.get(resource_name, []).append(policy_dict)

        return permissions_dict
