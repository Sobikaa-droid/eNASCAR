try:
    from .local import *
except ImportError:
    from .production import *
    print('No local.py was found. You must be on production.')
