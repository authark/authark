from typing import Any, Dict, Tuple
from flask import request
from flask_restful import Resource


class RegisterResource(Resource):

    def __init__(self, **kwargs: Any) -> None:
        self.auth_coordinator = kwargs['auth_coordinator']

    def post(self) -> Tuple[str, int]:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        try:
            user = self.auth_coordinator.register(username, email, password)
        except Exception as e:
            return '', 400

        response = 'Account Created: username<{0}> - email<{1}>'.format(
            username, email)

        return response, 201
