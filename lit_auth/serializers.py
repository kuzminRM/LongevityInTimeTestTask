from rest_framework.serializers import ModelSerializer

from lit_auth.models import User, OtpCode


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", 'email', "password", 'is_staff', 'is_superuser']
        extra_kwargs = {
            "password": {"write_only": True},
            'is_staff': {'read_only': True},
            'is_superuser': {'read_only': True},
        }

    def create(self, validated_data):
        return User.objects._create_user(commit=True, **validated_data)

    def update(self, instance: User, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class OtpCodeSerializer(ModelSerializer):
    class Meta:
        model = OtpCode
        fields = ['email']

    def create(self, validated_data):
        return OtpCode.send_auth_otp(validated_data['email'])

    def update(self, instance, validated_data):
        raise NotImplementedError()
