"""Users serializers."""

from django.contrib.auth import password_validation, authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from profiles.models import Profile


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            'pk',
            'first_name',
            'last_name',
            'email',
            'avatar',
        )


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    """
        Serializer for user log in endpoint.
    """

    def validate(self, data):
        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Credentials are not valid. Check email and password')

        self.context['user'] = user
        return data

    def create(self, data):
        """
            Generate or retrieve token.
        """
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class UserChangePasswordSerializer(serializers.Serializer):
    model = Profile

    """
        Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
