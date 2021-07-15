from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model

from .serializers import UserSerializer
from .permissions import IsLoggedInUser

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        permission_classes = []
        if self.action in ('list', 'create'):
            permission_classes = [AllowAny]
        elif self.action in ('retrieve', 'update', 'partial_update', 'destroy'):
            permission_classes = [IsLoggedInUser]
        return [permission() for permission in permission_classes]
