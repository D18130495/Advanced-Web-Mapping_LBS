import traceback

from django.contrib import auth
from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from django_restful_api.serializers import UserSerializer, GroupSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def login(request):
    result = True
    data = request.data
    username = data.get('username')
    password = data.get('password')

    user = auth.authenticate(username=username, password=password)

    if user is None:
        result = False
        errorInfo = u'Username or password is incorrect'
        return Response({"result": result, "token": None, "info": errorInfo})

    try:
        tokenObj = Token.objects.get(user_id=user.id)
    except FileNotFoundError as e:
        tokenObj = Token.objects.create(user=user)

    token = tokenObj.key

    return Response({"result": result, "token": token, "info": "Successfully logged in"})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes(())
def logout(request):
    result = True
    token = ''
    authInfo = request.META.get('HTTP_AUTHORIZATION')

    if authInfo:
        token = authInfo.split(' ')[1]

    try:
        token = Token.objects.get(key=token)
        token.delete()

        return Response({"result": result, "info": "Successfully logged out"})
    except FileNotFoundError as e:
        result = False
        print("token not exist")
        return Response({"result": result, "info": "Log out failed"})
