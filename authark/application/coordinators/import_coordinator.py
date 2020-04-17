from typing import List, Optional, Any
from ..utilities import QueryDomain
from ..services import ImportService
from ..repositories import (
    UserRepository, CredentialRepository, RoleRepository, RankingRepository,
    DominionRepository)
from ..models import User, Credential, Role, Ranking, Dominion


class ImportCoordinator:
    def __init__(self, import_service: ImportService,
                 user_repository: UserRepository,
                 credential_repository: CredentialRepository,
                 role_repository: RoleRepository,
                 ranking_repository: RankingRepository,
                 dominion_repository: DominionRepository) -> None:
        self.import_service = import_service
        self.user_repository = user_repository
        self.credential_repository = credential_repository
        self.role_repository = role_repository
        self.ranking_repository = ranking_repository
        self.dominion_repository = dominion_repository

    async def import_users(self, filepath: str, source: str,
                     password_field: str) -> None:
        users_list = self.import_service.import_users(
            filepath, source, password_field)
        for user, credential, roles in users_list:

            existing_user = await self._search_user(user)
            if existing_user:
                user = existing_user
                await self.user_repository.add(user)
            else:
                user = await self.user_repository.add(user)
            if credential:
                credential.user_id = user.id
                self._update_credential(credential)
            if roles:
                self._generate_ranking_user(roles, user)

    async def _search_user(self, user: User) -> Optional[User]:
        domain: QueryDomain = ['|', ('username', '=', user.username),
                               ('email', '=', user.email)]
        if user.id:
            domain = [('id', '=', user.id)]
        user_result = await self.user_repository.search(domain)
        if user_result:
            return user_result[0]
        return None

    async def _update_credential(self, credential: Credential):
        domain = [
            ('user_id', '=', credential.user_id),
            ('type', '=', 'password')]

        existing_credential = await self.credential_repository.search(domain)
        if existing_credential:
            credential.id = existing_credential[0].id
            result = await self.credential_repository.add(credential)
        else:
            await self.credential_repository.add(credential)

    async def _search_dominion(self, dominion: Dominion) -> Optional[Dominion]:
        domain = [('name', '=', dominion.name)]
        existing_dominion = await self.dominion_repository.search(domain)
        if existing_dominion:
            return existing_dominion[0]
        else:
            return None

    async def _create_ranking(self, role, user: User) -> None:
        if not role:
            return None
        ranking_domain = [('user_id', '=', user.id),
                          ('role_id', '=', role[0].id)]
        existing_ranking = await self.ranking_repository.search(ranking_domain)
        if not existing_ranking:
            ranking = Ranking(user_id=user.id,
                              role_id=role[0].id)
            await self.ranking_repository.add(ranking)

    async def _generate_ranking_user(self, roles: List[Any], user: User) -> None:
        for role, dominion in roles:
            existing_dominion = self._search_dominion(dominion)
            if existing_dominion:
                domain = [('name', '=', role.name)]
                existing_role = await self.role_repository.search(domain)
                self._create_ranking(existing_role, user)
