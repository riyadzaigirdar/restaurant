from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'name', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}
        read_only_fields = ['role']

    def create(self, validated_data):
        return get_user_model().objects.create_employee(**validated_data)

    def update(self, instance, validated_data):
        password = self.validated_data.pop('password', None)

        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
