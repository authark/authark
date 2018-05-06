"""
Authark entrypoint
"""
import sys
from authark.infra.web.base import create_app
from authark.infra.web.server import Application
from authark.infra.config.config import (
    DevelopmentConfig)


def main():
    try:
        config = DevelopmentConfig()
        config.resolve_registry()
        gunicorn_config = config['gunicorn']
    except Exception as e:
        sys.exit("Configuration loading error: {0} {1}".format(
            type(e), e))

    app = create_app(config)
    Application(app, gunicorn_config).run()


if __name__ == '__main__':
    main()