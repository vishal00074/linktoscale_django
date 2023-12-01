from django.shortcuts import redirect
from django.urls import reverse

class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        excluded_urls = ['/admin/']
        
        if request.path not in excluded_urls and 'admin' in request.path:
            if not request.user.is_authenticated:
                return redirect('admin')
        
        response = self.get_response(request)
        return response
        
        
        # if not request.user.is_authenticated and request.path != reverse('admin'):
        #     return redirect('admin')

        # response = self.get_response(request)
        # return response
