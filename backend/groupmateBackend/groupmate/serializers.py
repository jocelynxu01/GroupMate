from django.contrib.auth.models import User
from rest_framework import serializers
from .model_classes.Course import Course

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'email', 'password','role')

    def create(self, validated_data):
        
        role = validated_data.pop('role', None)
        print(role)
        user = User.objects.create_user(
            username = validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            
        )
        profile = user.profile
        if role:
            profile.role = role
        profile.save()
        return user

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'