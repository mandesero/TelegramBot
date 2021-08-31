

def database_handler(db_name):
    def outer(func):
        def wrapper(*args, **kwargs):
            with db_name:
                result = func(*args, **kwargs)
            return result
        return wrapper
    return outer
