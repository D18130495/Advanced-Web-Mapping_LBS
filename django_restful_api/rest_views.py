from rest_framework import generics, status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django_restful_api import serializers


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

# class RegisterUser(generics.CreateAPIView):
#     """
#     new user register
#     """
#     permission_classes = (AllowAny,)
#     serializer_class = serializers.RegisterSerializer


class ChangePassword(views.APIView):
    """
    change password
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            my_serializer = serializers.ChangePasswordSerializer(data=request.data)

            if my_serializer.is_valid():
                user = authenticate(
                    username=request.user.username,
                    password=my_serializer.validated_data['oldPassword']
                )

                if not user:
                    return Response({"result": False, "info": "Your old password is not correct, please input again"},
                                    status=status.HTTP_400_BAD_REQUEST)

                request.user.set_password(my_serializer.validated_data['newPassword'])
                request.user.save()

                return Response({"result": True, "info": "Successfully changed user password"},
                                status=status.HTTP_200_OK)
            else:
                return Response({"result": False, "info": "Server error"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": False, "info": "Server error"},
                            status=status.HTTP_400_BAD_REQUEST)
