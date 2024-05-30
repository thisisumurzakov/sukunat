from phonenumber_field.phonenumber import to_python
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField

from countries.models import Country

from .models import User


class BasePhoneSerializer(serializers.Serializer):
    phone_number = PhoneNumberField()

    def validate_phone_number(self, value):
        phone_number = to_python(value)
        if phone_number and not phone_number.is_valid():
            raise serializers.ValidationError("Invalid phone number format")

        # Check if the country code is supported
        country_code = f"+{phone_number.country_code}"
        if not Country.objects.filter(phone_code=country_code, is_active=True).exists():
            raise serializers.ValidationError(
                "Phone number from this country is not supported"
            )

        return value


class SendCodeSerializer(BasePhoneSerializer):
    pass


class VerifyCodeSerializer(BasePhoneSerializer):
    code = serializers.CharField(min_length=6, max_length=6)
    fcm_token = serializers.CharField(required=False)


class UserSerializer(serializers.ModelSerializer):
    profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "phone_number",
            "first_name",
            "last_name",
            "email",
            "is_email_verified",
            "profile_photo",
        )
        read_only_fields = ("phone_number", "is_email_verified", "id")

    def update(self, instance, validated_data):
        # Check if 'email' is in the validated data and differs from the current email
        if "email" in validated_data and instance.email != validated_data.get("email"):
            instance.email = validated_data.get("email")
            # Set is_email_verified to False as the email has changed, ensuring its verification status is reset
            instance.is_email_verified = False

        # Update first name and last name without altering is_email_verified based on frontend input
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)

        instance.save()
        return instance


class LogutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    fcm_token = serializers.CharField(required=False)
