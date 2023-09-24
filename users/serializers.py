from rest_framework.serializers import ModelSerializer
from users.models import User


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password is not None:
            user.set_password(password)
        user.save()
        return user
