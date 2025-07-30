from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from ..models import BlacklistedToken
from ..serializers.authSerializer import (
    SignupSerializer,
    LoginSerializer
)
from .token import JWTAuthentication
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt
from django.conf import settings

User = None

@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignupSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        payload = {"id": str(user.id)}  # UUID must be cast to str

        access_token = JWTAuthentication.generate_token(payload=payload)
        refresh_token = JWTAuthentication.generate_refresh_token(payload=payload)

        return Response({
            'accessToken': access_token,
            'refreshToken': refresh_token,
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        payload = {
            "id": user.id
        }

        access_token = JWTAuthentication.generate_token(payload=payload)
        refresh_token = JWTAuthentication.generate_refresh_token(payload=payload)

        return Response({
            'accessToken': access_token,
            'refreshToken': refresh_token
        }, status=status.HTTP_200_OK)

    print("Serializer errors:", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    refresh_token = request.data.get("refreshToken") or request.query_params.get("refreshToken")

    if not refresh_token:
        print('detail": "Refresh token is required.')
        return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
        if payload.get("type") != "refresh_token":
            print('detail": "Invalid token type.')
            return Response({"detail": "Invalid token type."}, status=status.HTTP_400_BAD_REQUEST)

        BlacklistedToken.objects.get_or_create(token=refresh_token)
        print('detail": "Invalid token type.')
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)

    except (InvalidTokenError, ExpiredSignatureError, jwt.DecodeError) as e:
        print('detail": "Invalid token.')
        return Response({"detail": f"Invalid token: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)