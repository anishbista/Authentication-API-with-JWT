from django.forms import ValidationError
from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Util


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["email", "name", "password", "password2", "tc"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password doesn't match."
            )
        return data

    def create(self, validate_data):

        return User.objects.create_user(**validate_data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]


class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )
    password2 = serializers.CharField(
        max_length=255, style={"input_type": "password"}, write_only=True
    )

    def validate(self, data):
        password = data.get("password")
        password2 = data.get("password2")
        user = self.context.get("user")
        if password != password2:
            raise serializers.ValidationError(
                "Password and Confirm Password didn't match"
            )
        user.set_password(password)
        user.save()
        return data


class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print(uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print(token)

            link = "http://localhost:8000/api/user/reset_password/" + uid + "/" + token
            print(link)
            body = "Click Following Link to Reset Your Password " + link
            data = {
                "subject": "Reset Your Password",
                "body": body,
                "to_email": user.email,
            }
            Util.send_email(data)
            return attrs

        else:
            raise serializers.ValidationError("Your are not registered user")


class UserPasswordResetSerializer(serializers.Serializer):
    try:
        password = serializers.CharField(
            max_length=255, style={"input_type": "password"}, write_only=True
        )
        password2 = serializers.CharField(
            max_length=255, style={"input_type": "password"}, write_only=True
        )

        def validate(self, data):
            password = data.get("password")
            password2 = data.get("password2")
            uid = self.context.get("uid")
            token = self.context.get("token")
            if password != password2:
                raise serializers.ValidationError(
                    "Password and Confirm Password didn't match"
                )
            id = urlsafe_base64_decode(uid)
            print(id)
            print((urlsafe_base64_decode(uid)))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise ValidationError("Token is not Valid or Expired")

            user.set_password(password)
            user.save()
            return data

    except DjangoUnicodeDecodeError as identifier:

        raise ValidationError("Token is not Valid or Expired")
