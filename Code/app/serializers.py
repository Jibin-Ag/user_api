# serializers.py
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'age']

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError('Name must not be empty.')
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Email must not be empty.')
        # Validate if email is unique
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(f"Email {value} is already registered.")
        return value

    def validate_age(self, value):
        if not (0 <= value <= 120):
            raise serializers.ValidationError('Age must be between 0 and 120.')
        return value
# from rest_framework import serializers
# from .models import User

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['name', 'email', 'age']
