#it should not be withdrawn from cookies, the resulting tokens should be recorded directly in the sessionstorage, withdrawn from there, verified from there and then deleted from there.
#
from django.middleware.csrf import CsrfViewMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.cache import SessionStore

class CustomSessionMiddleware(SessionMiddleware):
    def process_request(self, request):
        super().process_request(request)
        if request.session.session_key is None:
            request.session.create()
        request.session.modified = True
        request.session.save()

class CustomCsrfViewMiddleware(CsrfViewMiddleware):
    def _get_token(self, request):
        return request.session.get('csrf_token', None)

    def _set_token(self, request, token):
        request.session['csrf_token'] = token

    def _rotate_token(self, request):
        request.session['csrf_token'] = self._get_new_csrf_key()

    def _get_new_csrf_key(self):
        return self._salt_cipher_secret(self._get_new_csrf_string())

    def _get_new_csrf_string(self):
        return get_random_string(32, allowed_chars=ASCII_LETTERS + DIGITS)

    def _salt_cipher_secret(self, secret):
        return salted_hmac(
            self._salt,
            secret,
            secret=self._secret,
        ).hexdigest()

    def _get_token_from_request(self, request):
        return request.COOKIES.get(self._get_csrf_cookie_name(request), None)

    def _get_csrf_cookie_name(self, request):
        return 'csrftoken'

    def _get_csrf_cookie_domain(self, request):
        return None

    def _get_csrf_cookie_path(self, request):
        return '/'

    def _get_csrf_cookie_secure(self, request):
        return False

    def _get_csrf_cookie_httponly(self, request):
        return False

    def _get_csrf_cookie_samesite(self, request):
        return None

    def _get_csrf_cookie_max_age(self, request):
        return None

    def _get_csrf_cookie_set(self, request):
        return True

    def _get_csrf_token(self, request):
        return request.session.get('csrf_token', None)

    def _set_csrf_cookie(self, request, response):
        if not self._get_csrf_cookie_set(request):
            return
        response.set_cookie(
            self._get_csrf_cookie_name(request),
            self._get_csrf_token(request),
            max_age=self._get_csrf_cookie_max_age(request),
            domain=self._get_csrf_cookie_domain(request),
            path=self._get_csrf_cookie_path(request),
            secure=self._get_csrf_cookie_secure(request),
            httponly=self._get_csrf_cookie_httponly(request),
            samesite=self._get_csrf_cookie_samesite(request),
        )

    def _reject(self, request, reason):
        return self._get_failure_view()(request, reason=reason)

