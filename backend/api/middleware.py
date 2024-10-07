from django.db import transaction
from .messages import fast400


def atomic_transaction(func):
    def wrapper(*args, **kwargs):
        try:
            with transaction.atomic():
                return func(*args, **kwargs)
        except Exception as e:
            print(f"Transaction rolled back: {e}")
            return fast400

    return wrapper


class TransactionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        decorated_view_func = atomic_transaction(view_func)
        return decorated_view_func(request, *view_args, **view_kwargs)
