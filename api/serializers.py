from rest_framework import serializers
from base.models import UserProfile
from base.models import Product
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UpdateFavoritesSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    product_name = serializers.CharField(max_length=255)
    action = serializers.ChoiceField(choices=['add', 'remove'])

class UpdateCartSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    product_name = serializers.CharField(max_length=255)
    action = serializers.ChoiceField(choices=['add', 'remove'])

class UpdateOrderSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    product_names = serializers.ListField(child=serializers.CharField(max_length=255))  # Accepts multiple product names
    action = serializers.ChoiceField(choices=['add', 'remove'])

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['latitude', 'longitude', 'city', 'country','address','pincode', 'number', 'landmark']

class ItemSerializer(serializers.ModelSerializer):
    emailid = serializers.EmailField(write_only=True)
    confirmpassword = serializers.CharField(write_only=True)
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['username', 'password', 'emailid', 'confirmpassword','profile']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['confirmpassword']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        else:
            # Log the attrs to see the data
            print(attrs)
        return attrs


    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        validated_data['email'] = validated_data.pop('emailid')
        validated_data.pop('confirmpassword')
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
