from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Provider

User = get_user_model()


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
        fields = ('name', 'phone_number', 'language', 'currency')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    provider = ProviderSerializer(required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'provider',)
        extra_kwargs = {'password': {'write_only': True}, 'id': {'read_only': True}}

    def create(self, validated_data):
        provider_data = validated_data.pop('provider')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        Provider.objects.create(user=user, **provider_data)
        return user

    def update(self, instance, validated_data):
        provider_data = validated_data.pop('provider')
        provider = instance.provider

        instance.email = validated_data.get('email', instance.email)
        instance.save()

        provider.name = provider_data.get('name', provider.name)
        provider.phone_number = provider_data.get('phone_number', provider.phone_number)
        provider.language = provider_data.get('language', provider.language)
        provider.currency = provider_data.get('currency', provider.currency)
        provider.save()

        return instance
