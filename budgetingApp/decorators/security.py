from django.http import HttpResponseRedirect

import functools

def require_authentication(required: bool = True, redirect_url: str = '/'):
    """
    Enforces that the user IS / IS NOT authenticated before accessing an URL.

    This decorator ensures that restricted pages are not accessed without
    proper authentication. Furthermore, it can also ensure that pages such
    as login / register are unavailable to authenticated users.

    By default, enforces authentication and redirects to LOGIN users which are
    not authenticated.

    Arguments:
        - required (bool): denotes whether authentication is required or not
        - redirect_url (str): URL path to redirect in case condition is not met.
    """

    def wrapper(view_func):

        @functools.wraps(view_func)
        def wrapped(request, *args, **kwargs):
            if required and not request.user.is_authenticated:
                return HttpResponseRedirect(redirect_url)
            if not required and request.user.is_authenticated:
                return HttpResponseRedirect(redirect_url)

            return view_func(request, *args, **kwargs)
        return wrapped
    return wrapper