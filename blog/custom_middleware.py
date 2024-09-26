from django.contrib.auth import logout
from django.shortcuts import redirect

class AdminSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If an admin is logged in but tries to access the user pages, log them out
        if request.user.is_authenticated and request.user.is_superuser and 'admin' not in request.path:
            logout(request)
            return redirect('admin:index')

        # If a regular user tries to access admin, log them out
        if request.user.is_authenticated and not request.user.is_superuser and 'admin' in request.path:
            logout(request)
            return redirect('home')

        response = self.get_response(request)
        return response
