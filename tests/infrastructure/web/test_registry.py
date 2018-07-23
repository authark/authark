from pytest import fixture
from authark.application.coordinators.auth_coordinator import AuthCoordinator
from authark.infrastructure.config.registry import Registry, MemoryJwtRegistry
from authark.infrastructure.config.config import TrialConfig


def test_registry_type() -> None:
    assert issubclass(Registry, dict)


def test_registry_initialization() -> None:
    config = TrialConfig()
    registry = MemoryJwtRegistry(config=config)

    assert isinstance(registry['auth_coordinator'], AuthCoordinator)
