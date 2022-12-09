from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'first_name', 'last_name', 'email']


class Login(serializers.Serializer):
    """
    user login
    """
    username = serializers.CharField(
        required=True
    )

    password = serializers.CharField(
        required=True,
        validators=[validate_password]
    )

    def validate(self, data):
        return data


class Logout(serializers.Serializer):
    """
    user logout
    """
    class Meta:
        model = User


class RegisterUserSerializer(serializers.Serializer):
    """
    serializer handle new user register
    """
    username = serializers.CharField(
        write_only=True,
        required=True,
        # validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    confirmPassword = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, data):
        """
        check whether two password are same
        :param data: password
        :return: return password if same, else raise error
        """
        if data['password'] != data['confirmPassword']:
            raise serializers.ValidationError("Password is not same")

        return data


class UpdateProfileSerializer(serializers.Serializer):
    """
    serializer handle update profile
    """
    firstName = serializers.CharField(
        required=False
    )

    lastName = serializers.CharField(
        required=False
    )

    email = serializers.CharField(
        required=False
    )

    def to_internal_value(self, data):
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    serializer handle change password
    """
    oldPassword = serializers.CharField(
        write_only=True,
        required=True
    )

    newPassword = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )

    confirmPassword = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, data):
        """
        check whether two password are same
        :param data: password
        :return: return password if same, else raise error
        """
        if data['newPassword'] != data['confirmPassword']:
            raise serializers.ValidationError("Password is not same")

        return data
