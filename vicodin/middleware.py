from django.shortcuts import redirect
from django.urls import resolve
from django.utils.deprecation import MiddlewareMixin

class LastVisitedMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.path.startswith('/admin/') or request.path.startswith('/static/'):
            return

        try:
            resolve(request.path)
            request.session['last_valid_url'] = request.path
        except:
            pass

    def process_response(self, request, response):
        if response.status_code == 404:
            last_valid_url = request.session.get('last_valid_url', '/')
            return redirect(last_valid_url)
        return response