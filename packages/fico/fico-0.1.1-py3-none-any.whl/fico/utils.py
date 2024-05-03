from functools import wraps

optional_dependency_status = {}

class MissingDependencyError(Exception):
    pass


def requires_table(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if not optional_dependency_status.get("table", False):
            raise MissingDependencyError("This feature requires an optional dependency. Install fico[table] to enable this feature.")

        return f(*args, **kwds)
    
    return wrapper