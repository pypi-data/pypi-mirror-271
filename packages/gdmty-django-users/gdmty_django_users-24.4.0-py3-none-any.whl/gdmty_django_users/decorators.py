from functools import wraps
from gdmty_django_recaptcha_enterprise.decorators import requires_recaptcha_token
from .settings import ENABLE_RECAPTCHA


def recaptcha_verify(action=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if ENABLE_RECAPTCHA:
                return requires_recaptcha_token(action)(view_func)(request, *args, **kwargs)
            else:
                return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
