from rest_framework.viewsets import ModelViewSet
from users.models import User
from users.permissions import IsOwnerOrReadOnly
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
