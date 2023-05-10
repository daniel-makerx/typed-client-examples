import logging

from smart_contracts import helloworld, lifecycle, testing_app, voting

logger = logging.getLogger(__name__)

# define contracts to build and/or deploy
contracts = [helloworld.app, voting.app, lifecycle.app, testing_app.app]
