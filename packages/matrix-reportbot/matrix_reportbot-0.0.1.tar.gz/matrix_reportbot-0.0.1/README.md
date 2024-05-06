# Matrix-ReportBot

[![Support Private.coffee!](https://shields.private.coffee/badge/private.coffee-support%20us!-pink?logo=coffeescript)](https://private.coffee)
[![PyPI](https://shields.private.coffee/pypi/v/matrix-reportbot)](https://pypi.org/project/matrix-reportbot/)
[![PyPI - Python Version](https://shields.private.coffee/pypi/pyversions/matrix-reportbot)](https://pypi.org/project/matrix-reportbot/)
[![PyPI - License](https://shields.private.coffee/pypi/l/matrix-reportbot)](https://pypi.org/project/matrix-reportbot/)
[![Latest Git Commit](https://shields.private.coffee/gitea/last-commit/privatecoffee/matrix-reportbot?gitea_url=https://git.private.coffee)](https://git.private.coffee/privatecoffee/matrix-reportbot)

This is a simple bot that can be used to display incoming moderation reports in a Matrix room.

## Installation

```bash
pip install matrix-reportbot
```

Create a configuration file in `config.ini` based on the [config.dist.ini](config.dist.ini) provided in the repository.

At the very least, you need to provide the following configuration:

```ini
[Matrix]
Homeserver = http://your-homeserver.example.com
AccessToken = syt_YourAccessTokenHere
RoomId = !yourRoomId:your-homeserver.example.com
```

Note: The AccessToken must be for a admin user, because the bot needs to be able to read the moderation events.

We recommend using pantalaimon as a proxy, because the bot itself does not support end-to-end encryption.

You can start the bot by running:

```bash
reportbot
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
