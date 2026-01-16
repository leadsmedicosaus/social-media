class SocialUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.social_user_id = request.user.pk if request.user.is_authenticated else None

        return self.get_response(request)
