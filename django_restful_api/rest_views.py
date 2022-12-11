from django.utils import timezone
from rest_framework import generics, status
from rest_framework import views, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

from django_restful_api import serializers, models


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]


class Login(generics.CreateAPIView):
    """
    API endpoint that allows users login, accept all the request
    """
    serializer_class = serializers.Login
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            my_serializer = serializers.Login(data=request.data)

            # serializer passes the password format check
            if my_serializer.is_valid():
                user = authenticate(
                    username=my_serializer.validated_data['username'],
                    password=my_serializer.validated_data['password']
                )

                # username and password not match
                if not user:
                    return Response({"result": False, "info": "Username or password is incorrect"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # user exist, find token or create token
                try:
                    tokenObj = Token.objects.get(user_id=user.id)
                except Exception as e:
                    tokenObj = Token.objects.create(user=user)

                # update last_login time
                user.last_login = timezone.now()
                user.save(update_fields=['last_login'])

                token = tokenObj.key

                return Response(
                    {"result": True, "token": token, "user": user.username, "info": "Successfully logged in"},
                    status=status.HTTP_200_OK)

            return Response({"result": False, "info": "Password format is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": False, "info": "Server error, login failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Logout(views.APIView):
    """
    API endpoint that allows users logout, accept all the request
    """
    permission_classes = (AllowAny,)
    serializer_class = serializers.Logout

    def get(self, request, *args, **kwargs):
        # get user token
        authInfo = request.META.get('HTTP_AUTHORIZATION')

        # parse user token
        if authInfo != 'Token null':
            token = authInfo.split(' ')[1]
        else:
            # token does not exist
            return Response({"result": False, "info": "Token does not provided, logged out"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=request.user.username)

            if not user:
                # user does not exist
                return Response({"result": False, "info": "User does not exist, logged out"},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                Token.objects.get(key=token)
                # successfully logged in
                return Response({"result": True, "info": "Successfully logged out"}, status=status.HTTP_200_OK)
            except Exception as e:
                # token does not exist in the server
                return Response({"result": False, "info": "Token does not exist in the server, logged out"},
                                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": False, "info": "Server error, logged out"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RegisterUser(views.APIView):
    """
    API endpoint that allow new user register, accept all the request
    """
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request, *args, **kwargs):
        try:
            my_serializer = serializers.RegisterUserSerializer(data=request.data)

            # serializer passes the password format check
            if my_serializer.is_valid():
                try:
                    User.objects.create_user(
                        username=my_serializer.validated_data['username'],
                        password=my_serializer.validated_data['password']
                    )

                    # successfully logged in
                    return Response(
                        {"result": True, "info": "Successfully signed up, automatic login in three seconds"},
                        status=status.HTTP_200_OK)
                except Exception as e:
                    # User.objects.create_user failed
                    return Response({"result": False, "info": "Server error, register failed"},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # username already exist
            return Response({"result": False, "info": "Username already exists in the system, please input again"},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": False, "info": "Server error, register failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetCurrentUserInfo(views.APIView):
    """
    API endpoint that to get current login user information, only accept authenticated
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user.username)

            return Response({"result": True, "firstName": user.first_name, "lastName": user.last_name,
                             "email": user.email, "info": "Successfully get user information"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": False, "info": "Server error, get current user information failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateProfile(views.APIView):
    """
    API endpoint that update user profile, only accept authenticated
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.UpdateProfileSerializer

    def post(self, request, *args, **kwargs):
        try:
            my_serializer = serializers.UpdateProfileSerializer(data=request.data)

            # serializer passes the format check
            if my_serializer.is_valid():
                # update user profile
                User.objects.filter(username=request.user.username) \
                    .update(first_name=my_serializer.validated_data['firstName'],
                            last_name=my_serializer.validated_data['lastName'],
                            email=my_serializer.validated_data['email'])

                # successfully update user profile
                return Response({"result": True, "firstName": my_serializer.validated_data['firstName'],
                                 "lastName": my_serializer.validated_data['lastName'],
                                 "email": my_serializer.validated_data['email'],
                                 "info": "Successfully updated user information"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": False, "info": "Server error, update profile failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePassword(views.APIView):
    """
    API endpoint that change password, only accept authenticated
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        try:
            my_serializer = serializers.ChangePasswordSerializer(data=request.data)

            # serializer passes the format check
            if my_serializer.is_valid():
                user = authenticate(
                    username=request.user.username,
                    password=my_serializer.validated_data['oldPassword']
                )

                if not user:
                    # old password not correct
                    return Response({"result": False, "info": "Your old password is not correct, please input again"},
                                    status=status.HTTP_400_BAD_REQUEST)

                # set new password
                request.user.set_password(my_serializer.validated_data['newPassword'])
                request.user.save()

                # successfully changed password
                return Response({"result": True, "info": "Successfully changed user password"},
                                status=status.HTTP_200_OK)
            else:
                # new password format is invalid
                return Response({"result": False, "info": "New password format is invalid"},
                                status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": False, "info": "Server error, change password failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateLocation(views.APIView):
    """
    API endpoint that update user location when click on the map, only accept authenticated
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # find user profile
            user_profile = models.Profile.objects.get(user=request.user)

            if not user_profile:
                return Response({"result": False, "info": "Get user failed"},
                                status=status.HTTP_400_BAD_REQUEST)

            # parse location and save to profile
            location = request.data['location'].split(",")
            location = [float(part) for part in location]
            location = Point(location, srid=4326)

            user_profile.last_location = location
            user_profile.save()

            # successfully updated current location
            return Response({"result": True, "info": "Successfully updated location"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"result": False, "info": "Server error, update location failed"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
