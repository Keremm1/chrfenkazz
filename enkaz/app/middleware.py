from django.http import HttpResponseForbidden

class IPBanMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        banned_ips = []
        if request.META['REMOTE_ADDR'] in banned_ips:
            return HttpResponseForbidden("Your IP is banned.")
        response = self.get_response(request)
        return response