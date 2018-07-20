from json import dumps
from pytest import fixture
from authark.application.models.user import User
from authark.application.repositories.user_repository import UserRepository
from authark.infrastructure.data.json_user_repository import JsonUserRepository


@fixture
def user_repository(tmpdir) -> JsonUserRepository:
    user_dict = {
        "valenep": vars(User('valenep', 'valenep@gmail.com', "PASS1")),
        "tebanep": vars(User('tebanep', 'tebanep@gmail.com', "PASS2")),
        "gabecheve": vars(User('gabecheve', 'gabecheve@gmail.com', "PASS3"))
    }

    file_path = str(tmpdir.mkdir("authark").join('authark_data.json'))
    with open(file_path, 'w') as f:
        data = dumps({'users': user_dict})
        f.write(data)

    user_repository = JsonUserRepository(file_path=file_path)

    return user_repository


def test_json_user_repository_implementation() -> None:
    assert issubclass(JsonUserRepository, UserRepository)


def test_json_user_repository_get_user(
        user_repository: JsonUserRepository) -> None:

    user = user_repository.get("valenep")

    assert user and user.username == "valenep"
    assert user and user.email == "valenep@gmail.com"