import functools
import time

from exception import NotFoundAttributeException
from util import create_logger

log = create_logger('retry_util')


def retry_wrap(attempt=10, wait=1, retryable_exceptions=()):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for cnt in range(attempt):
                log.info(f' └─ trying {func.__name__}() [{cnt + 1} / {attempt}]')

                try:
                    result = func(*args, **kwargs)
                    log.info(f'   └─ in retry_wrap(), {func.__name__}() returned {result}')
                    if result:
                        return result
                except retryable_exceptions as e:
                    pass
                except Exception as e:
                    raise e

                time.sleep(wait)
            log.info(f'   └─ {func.__name__} finally has been failed')
            raise NotFoundAttributeException
        return wrapper
    return decorator
