from fastapi.exceptions import HTTPException


def handle_http_exceptions(exceptions_map: dict[Exception, HTTPException]):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                result = await func(*args, **kwargs)
                return result
            except Exception as e:
                if e not in exceptions_map.keys():
                    raise e
            raise exceptions_map[exceptions_map]

        return wrapper

    return decorator
