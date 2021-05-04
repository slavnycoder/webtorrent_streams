from knox.auth import TokenAuthentication as KnoxTokenAuthentication


class TokenAuthentication(KnoxTokenAuthentication):

    def validate_user(self, auth_token):
        return auth_token.user, auth_token
