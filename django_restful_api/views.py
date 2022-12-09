from django.contrib import auth
from django.contrib.auth.models import User, Group
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response


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
        return Response({"result": result, "token": None, "info": "Username or password is incorrect"})

    try:
        tokenObj = Token.objects.get(user_id=user.id)
    except Exception as e:
        tokenObj = Token.objects.create(user=user)

    token = tokenObj.key

    return Response({"result": result, "token": token, "user": str(user), "info": "Successfully logged in"})


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
    except Exception as e:
        result = False
        print("token not exist")
        return Response({"result": result, "info": "Log out failed"})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def signup(request):
    result = True
    data = request.data
    username = data.get('username')
    password = data.get('password')

    try:
        User.objects.get(username=username)

        result = False
        return Response({"result": result, "info": "Username already exists in the system, please input again"})
    except Exception as e:
        User.objects.create(username=username, password=make_password(password))
        return Response({"result": result, "info": "Successfully signed up, automatic login in three seconds"})


@api_view(['GET'])
@permission_classes((AllowAny,))
@authentication_classes(())
def get_user_info_by_token(request):
    result = True
    token = request.GET.get('0')

    if token is None:
        result = False
        return Response({"result": result, "info": "Can not get user information"})
    else:
        tokenObj = Token.objects.get(key=token)
        userInfo = User.objects.get(id=tokenObj.user_id)
        return Response({"result": result, "firstName": userInfo.first_name, "lastName": userInfo.last_name,
                         "email": userInfo.email, "info": "Successfully get user information"})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def update_profile(request):
    result = True
    data = request.data
    token = data.get('token')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    email = data.get('email')

    if token is None:
        result = False
        return Response({"result": result, "info": "Update profile failed, unauthorized user"})
    else:
        tokenObj = Token.objects.get(key=token)
        userId = User.objects.filter(id=tokenObj.user_id).update(first_name=firstName, last_name=lastName, email=email)
        userInfo = User.objects.get(id=userId)
        return Response({"result": result, "firstName": userInfo.first_name, "lastName": userInfo.last_name,
                         "email": userInfo.email, "info": "Successfully updated user information"})


@api_view(['POST'])
@permission_classes((AllowAny,))
@authentication_classes(())
def change_password(request):
    result = True
    data = request.data
    print(data)
    token = data.get('token')
    oldPassword = data.get('oldPassword')
    newPassword = data.get('newPassword')

    if token is None:
        result = False
        return Response({"result": result, "info": "Change password failed, unauthorized user"})
    else:
        tokenObj = Token.objects.get(key=token)
        userInfo = User.objects.get(id=tokenObj.user_id)

        if check_password(oldPassword, userInfo.password):
            User.objects.filter(id=tokenObj.user_id).update(password=make_password(newPassword))
            return Response({"result": result, "info": "Successfully changed user password"})
        else:
            result = False
            return Response({"result": result, "info": "Your old password is not correct, please input again"})
