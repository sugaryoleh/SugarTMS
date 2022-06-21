from django.contrib.auth.models import User
from rest_framework.serializers import HyperlinkedModelSerializer, CharField, EmailField, BooleanField, Serializer

from app.models.users.profile import Profile


class ProfileSerializer(Serializer):
    first_name = CharField(required=True, allow_blank=False, max_length=150)
    last_name = CharField(required=True, allow_blank=False, max_length=150)
    email = EmailField(required=True, allow_null=False)
    is_superuser = BooleanField(default=False)
    is_coordinator = BooleanField(default=False)

    def create(self, validated_data):

        user = User.objects.create_user(first_name=validated_data['first_name'], last_name=validated_data['last_name'],
                                        username=validated_data['email'], email=validated_data['email'],
                                        password=validated_data['email'])
        return Profile.objects.get(user=user)

    def update(self, instance, validated_data):
        user = User.objects.get(pk=instance.user.id)
        user.first_name = validated_data.get('first_name', user.first_name)
        user.last_name = validated_data.get('last_name', user.last_name)
        user.email = validated_data.get('email', user.email)
        user.is_superuser = validated_data.get('is_superuser', user.is_superuser)
        instance.is_coordinator = validated_data.get('is_superuser', instance.is_coordinator)
        user.save()
        instance.save()
        return instance
