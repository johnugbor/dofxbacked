from django.contrib.auth import get_user_model

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer




class CustomRegisterSerializer( RegisterSerializer, serializers.ModelSerializer):

    '''Custom serializer to handle registration'''
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
             'email', 'password1',
            'password2','full_name','currency','phone_number'
        ]

    


class CustomUserDetailsSerializer( UserDetailsSerializer):

    '''Custom `user` detail serializer'''
    class Meta:
        model = get_user_model()
        exclude = [
            'created_at',
            'updated_at',
          
            'password'
        ]
        read_only_fields = ['email', 'id']


