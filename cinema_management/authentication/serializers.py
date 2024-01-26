# from rest_framework import serializers
# from .models import User

# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    
#     class Meta:
#         model = User
#         fields = ['email', 'username', 'password']

#     def validate(self, attrs):
#         email=attrs.get('email', '')
#         username=attrs.get('username', '')

#         if not username.isalnum():
#             raise serializers.ValidationError('The username should only contain a alphanumeric characters')
#         return attrs
        
#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)

from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=6, write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(max_length=68, min_length=6, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password_confirm']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username should only contain alphanumeric characters')

        if password != password_confirm:
            raise serializers.ValidationError('The passwords do not match')

        return attrs

    def create(self, validated_data):
        # Remove the 'password_confirm' field before creating the user
        validated_data.pop('password_confirm', None)
        return User.objects.create_user(**validated_data)
