from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate
from rest_framework import exceptions

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #fields = ('first_name','last_name','email','url')
        fields = '__all__'

class TimesheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timesheet
        fields = ["job","date","hours","employee","id"]

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username",'')
        password = data.get("password",'')

        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    msg = "user is deactivated"
                    raise exceptions.ValidationError(msg)

            else:
                msg = "Unable to login with given credentials "
                raise exceptions.ValidationError(msg)
        else:
            msg = "Must provide username and password"
            raise exceptions.ValidationError(msg)
        return data


