import functools
import logging

from pydockerhub.api_calls.errors import ApiCallError
from pydockerhub.error import PyDockerHubError
from pydockerhub.hub.errors import DockerHubError


def handle_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger = logging.getLogger("pydockerhub")
        logger.setLevel(logging.WARNING)

        try:
            return func(*args, **kwargs)
        except ApiCallError as e:
            logger.error(f'Error during HTTP call: {str(e)}')
            raise
        except DockerHubError as e:
            logger.error(f'Error during PyDockerHub call: {str(e)}')
            raise
        except PyDockerHubError as e:
            logger.error(f'PyDockerHub error: {str(e)}')
            raise
        except Exception as e:
            logger.error(f'General error: {str(e)}')
            raise

    return wrapper
