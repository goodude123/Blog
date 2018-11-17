from django.urls import reverse
from django.shortcuts import redirect

def prevent_logged(function):
    '''Prevent view logged users, redirect them to main page.'''
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('cms:main'))
        return function(request, *args, **kwargs)

    wrapper.__doc__ = function.__doc__
    wrapper.__name__ = function.__name__
    return wrapper
