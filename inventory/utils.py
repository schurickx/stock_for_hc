from rest_framework.authentication import SessionAuthentication


# To not perform the csrf check previously happening
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return