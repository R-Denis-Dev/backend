from rest_framework.authentication import BaseAuthentication


class BearerToken(BaseAuthentication):
    keyword='Bearer'