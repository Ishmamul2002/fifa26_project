# This file is no longer needed since we removed JWT
# All JWT decorators have been removed from routes

def dummy_protection(f):
    """Dummy decorator - does nothing"""
    return f