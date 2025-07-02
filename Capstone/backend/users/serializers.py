from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, ProfessorProfile


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'department')
        read_only_fields = ('id',)


class ProfessorProfileSerializer(serializers.ModelSerializer):
    """Serializer for ProfessorProfile model"""
    
    user = UserSerializer(read_only=True)
    available_slots = serializers.ReadOnlyField()
    
    class Meta:
        model = ProfessorProfile
        fields = ('user', 'research_domains', 'bio', 'total_slots', 'filled_slots', 'available_slots')


class LoginSerializer(serializers.Serializer):
    """Serializer for user login"""
    
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled')
        else:
            raise serializers.ValidationError('Must include username and password')
        
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role', 'phone_number', 'department', 'password', 'password_confirm')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user 