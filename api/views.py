from rest_framework.generics import CreateAPIView

class FollowCreate(CreateAPIView):
    def post(self, request, *args, **kwargs):
        
        return self.create(request, *args, **kwargs)