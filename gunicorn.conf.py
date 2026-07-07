"""Gunicorn server hooks.

post_fork runs inside each freshly-forked WORKER process, which is what
actually serves HTTP traffic - see the docstring in app.py for why starting
the background data-loading thread at plain module-import time doesn't work
(it ends up running in the master process instead, which never handles
requests).
"""


def post_fork(server, worker):
    from app import start_background_loading
    start_background_loading()
