from rest_framework import serializers
import re
import bcrypt
from django.contrib.auth.password_validation import validate_password
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'first_name', 'last_name', 'email', 'password']

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except serializers.ValidationError as e:
            raise serializers.ValidationError(str(e))

        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter.")

        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter.")

        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Password must contain at least one digit.")

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Password must contain at least one special character.")

        return value

    def create(self, validated_data):
        # Hash the password before saving
        validated_data['password'] = self._hash_password(
            validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Hash the password before saving
        validated_data['password'] = self._hash_password(
            validated_data['password'])
        return super().update(instance, validated_data)

    def _hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14)).decode('utf-8')
