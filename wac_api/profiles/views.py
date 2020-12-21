from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action, api_view
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from profiles.serializers import UserLoginSerializer, UserModelSerializer, UserChangePasswordSerializer

from profiles.models import Profile

from profiles.permissions import IsHisUser


class UserViewSet(viewsets.GenericViewSet):
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = UserModelSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        """
            User sign in
        """
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)


class EditViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
        User edit profile
    """
    queryset = Profile.objects.filter(is_active=True)
    serializer_class = UserModelSerializer
    permission_classes = IsAuthenticated, IsHisUser


class ChangePasswordView(UpdateAPIView):
    """
        User change password
    """
    serializer_class = UserChangePasswordSerializer
    model = Profile
    permission_classes = (IsAuthenticated, IsHisUser)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': "Wrong password"
                }, status=status.HTTP_400_BAD_REQUEST)
            # Set new password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully'
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)