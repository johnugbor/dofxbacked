from django.contrib.auth import get_user_model

from rest_framework import serializers

from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import UserDetailsSerializer




class CustomRegisterSerializer( RegisterSerializer, serializers.ModelSerializer):

    '''Custom serializer to handle registration'''
    full_name = serializers.CharField(write_only=True)
    currency  = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = [
             'email', 'password1',
            'password2','full_name','currency','phone_number'
        ]

    def custom_signup(self,request,user):
        user.full_name =self.validated_data.get('full_name','')
        user.currency = self.validated_data.get('currency','')
        user.phone_number =self.validated_data.get('phone_number','')
        user.save(update_fields=['full_name','currency','phone_number'])



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


