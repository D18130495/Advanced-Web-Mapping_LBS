from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


# class RegisterSerializer(serializers.Serializer, ABC):
#     """
#     serializer handle new user register
#     """
#     print(123)


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
