from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CreateUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        min_length=1, max_length=32,
        validators=[UniqueValidator(User.objects.all())]
    )
    email = serializers.EmailField(
        required=False,
        validators=[UniqueValidator(User.objects.all())]
    )
    password = serializers.CharField(
        required=True, min_length=8, write_only=True
    )
    password_2 = serializers.CharField(
        required=True, min_length=8, write_only=True
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_2')

    def validate_password(self, value):
        data = self.get_initial()
        password_2 = data.get('password_2')
        if value != password_2:
            raise serializers.ValidationError('Passwords must match.')
        return value

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data.get('email', '')
        password = validated_data['password']
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        return user


class LoginUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate(self, data):
        user = User.objects.filter(email__iexact=data['email']).first()
        if not user:
            raise serializers.ValidationError('Unknown user')
        return data
