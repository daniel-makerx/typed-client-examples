import logging

from smart_contracts import helloworld, lifecycle, voting

logger = logging.getLogger(__name__)

# define contracts to build and/or deploy
contracts = [helloworld.app, voting.app, lifecycle.app]
