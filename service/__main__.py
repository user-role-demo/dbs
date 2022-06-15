from service.app import create_app
from service.config import app_config


def main():
    app = create_app()

    app.run(
        port=app_config.app_port,
        host=app_config.app_host,
        debug=app_config.debug,
    )


if __name__ == '__main__':
    main()
