from django.http import HttpResponse
from django.shortcuts import redirect


# brak autoryzacji
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('image_list')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

#  blokować strony dla wybranej grupy
def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorized to view this page')
        return wrapper_func
    return decorator

def Enterprise_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.uploaded_by.groups.all()[0].name

        if group == 'Basic':
            return redirect('login')

        if group == 'Enterprise':
            return view_func(request, *args, **kwargs)

    return wrapper_function


















