from .config import Config


class DevelopmentConfig(Config):
    def __init__(self):
        super().__init__()
        self['mode'] = 'DEV'
        self['gunicorn'].update({
            'debug': True,
            'accesslog': '-',
            'loglevel': 'debug'
        })
        self['factory'] = 'MemoryFactory'
        self['providers'] = {
            "ExpressionParser": {
                "method": "expression_parser"
            },
            "UserRepository": {
                "method": "memory_user_repository"
            },
            "CredentialRepository": {
                "method": "memory_credential_repository"
            },
            "DominionRepository": {
                "method": "memory_dominion_repository"
            },
            "RoleRepository": {
                "method": "memory_role_repository"
            },
            "RankingRepository": {
                "method": "memory_ranking_repository"
            },
            "HashService": {
                "method": "memory_hash_service"
            },
            "AccessTokenService": {
                "method": "memory_access_token_service"
            },
            "RefreshTokenService": {
                "method": "memory_refresh_token_service"
            },
            "AccessService": {
                "method": "standard_access_service"
            },
            "AuthCoordinator": {
                "method": "auth_coordinator"
            },
            "ManagementCoordinator": {
                "method": "management_coordinator"
            },
            "AutharkReporter": {
                "method": "standard_authark_reporter"
            },
            "ComposingReporter": {
                "method": "standard_composing_reporter"
            }
        }