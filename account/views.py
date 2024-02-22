from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from .renders import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken


# To generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Registration Successful."},
                status=status.HTTP_201_CREATED,
            )
        print(str(serializer.errors))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            password = serializer.data.get("password")
            user = authenticate(email=email, password=password)
            if user:
                token = get_tokens_for_user(user)
                return Response(
                    {"token": token, "msg": "Login Successful."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {
                        "errors": {
                            "non_field_errors.": ["Email or Password is not valid"]
                        }
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        return Response(serializer.errors, status=status.HTTP_200_OK)
