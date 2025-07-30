from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

# Signup Serializer for User Registration
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'username']

    def create(self, validated_data):

        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=validated_data.get('username'),
        )
        return user

# Login Serializer to Validate Credentials
class LoginSerializer(serializers.Serializer):  
    email = serializers.EmailField() 
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, attrs):

        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError("Both email and password are required")

        user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Invalid credentials")

        attrs['user'] = user
        return attrs