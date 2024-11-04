from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth.password_validation import validate_password
from .tasks import send_otp_task
from .utils import generate_and_store_otp

from users.models import CustomUser






class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField() 
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    phone_number = serializers.CharField(validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    is_paid = serializers.BooleanField(default=False)
    country = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        data.pop('confirm_password')
        if not data.get('first_name'):
            raise serializers.ValidationError("First name is required.")
        if not data.get('last_name'):
            raise serializers.ValidationError("Last name is required.")
        if not data.get('username'):
            raise serializers.ValidationError("Username is required.")
        if CustomUser.objects.filter(username=data.get('username')).exists():
            raise serializers.ValidationError("Username is already taken.")
        if not data.get('email'):
            raise serializers.ValidationError("Email is required.")
        if CustomUser.objects.filter(email=data.get('email')).exists():
            raise serializers.ValidationError("Email is already taken.")
        if not data.get('password'):
            raise serializers.ValidationError("Password is required.")
        if not data.get('phone_number'):
            raise serializers.ValidationError("Phone number is required.")
        if CustomUser.objects.filter(phone_number=data.get('phone_number')).exists():
            raise serializers.ValidationError("Phone number is already registered.")
        
        data['country'] = data.get('country', '')
        data['is_paid'] = data.get('is_paid', False)

        return data
    
    def create(self, validated_data):  
        country=validated_data['country']
        role='user'

        user = CustomUser.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            country=validated_data['country'],
            role=role
        )
        print("Plain text password:", validated_data['password'])
        user.set_password(validated_data['password'])
        user.save()

        # user.is_active = False
        user.save()

        print(validated_data, "validated=================")
#         # genarating otp
#         otp = generate_and_store_otp(user.id)
#         print("============", otp, "============ otp")
#         # sent otp to celery
#         send_otp_task.delay(user.email, otp)

        return validated_data




class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email:
            raise serializers.ValidationError("email is required.")
        if not password:
            raise serializers.ValidationError("Password is required.")

        if not CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError("User not Found.")

        return data

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'email', 'profile_picture','country']
        
        

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"confirm_password": "New password and confirm password don't match."})
        return attrs