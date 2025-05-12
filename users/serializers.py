from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import UserProfile, CustomUser, UserAssignment

from djoser.serializers import TokenCreateSerializer
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        print(f"Authentication attempt for email: {email}")

        # Log the password length for debugging purposes (do not log the actual password)
        print(
            f"Password length: {len(password) if password else 'No password provided'}"
        )

        # Authenticate using the email as the username
        user = authenticate(username=email, password=password)

        # Check if the authentication failed
        if user is None:
            print("Authentication failed: No user found or incorrect password.")
            raise ValidationError(
                {
                    "message": "Invalid credentials.",
                    "email": [
                        "No user found with this email address or password is incorrect."
                    ],
                }
            )

        # Check if the user is inactive
        if not user.is_active:
            print("Authentication failed: User account is inactive.")
            raise ValidationError(
                {
                    "message": "Account inactive.",
                    "email": [
                        "Your account has not been verified. Please check your email for the verification link."
                    ],
                }
            )

        print("Authentication succeeded. User ID:", user.id)

        # Create or get the existing auth token for the user
        token, created = Token.objects.get_or_create(user=user)
        print(token)

        # Ensure the token has a user associated
        if not user or token.user is None:
            print("Token creation failed. User is not associated with the token.")
            raise ValidationError(
                {
                    "message": "Token generation failed.",
                    "detail": ["Token could not be created. Please try again."],
                }
            )

        print("Token generated:", token.key)
        return {"auth_token": token.key}


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'email', 'first_name', 'last_name', 'password']
#         # fields = '__all__'
#         extra_kwargs = {
#             'password': {'write_only': True, 'required': True},  # Password is required
#             'email': {'required': True},  # Email is required
#             'first_name': {'required': False},  # First name is optional
#             'last_name': {'required': False},  # Last name is optional
#         }

#     def create(self, validated_data):
#         # Automatically set the username as the first name
#         validated_data['username'] = validated_data.get('first_name')
#         user = CustomUser(**validated_data)
#         user.set_password(validated_data['password'])  # Hash the password
#         user.save()
#         return user


class UserSerializer(serializers.ModelSerializer):
    # user_intent = serializers.ChoiceField(
    #     choices=UserProfile.INTENT_CHOICES, required=False, allow_null=True
    # )
    # role = serializers.ChoiceField(
    #     choices=UserProfile.ROLE_CHOICES, required=False, allow_null=True
    # )

    # class Meta:
    #     model = CustomUser
    #     fields = [
    #         "id",
    #         "email",
    #         "first_name",
    #         "last_name",
    #         "password",
    #         "user_intent",
    #         "role",
    #     ]
    #     extra_kwargs = {
    #         "password": {"write_only": True, "required": True},  # Password is required
    #         "email": {"required": True},  # Email is required
    #         "first_name": {"required": False},  # First name is optional
    #         "last_name": {"required": False},  # Last name is optional
    #     }

    # def create(self, validated_data):
    #     user_intent = validated_data.pop("user_intent", None)
    #     role = validated_data.pop("role", None)

    #     validated_data["username"] = validated_data.get("first_name")
    #     user = CustomUser(**validated_data)
    #     user.set_password(validated_data["password"])  # Hash the password

    user_intent = serializers.ChoiceField(
        choices=UserProfile.INTENT_CHOICES, required=False, allow_null=True
    )
    role = serializers.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, required=False, allow_null=True
    )
    purpose = serializers.ChoiceField(
        choices=UserProfile.PURPOSE_CHOICES, required=False, allow_null=True
    )

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "user_intent",
            "role",
            "purpose",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def create(self, validated_data):
        user_intent = validated_data.pop("user_intent", None)
        role = validated_data.pop("role", None)
        purpose = validated_data.pop("purpose", None)

        validated_data["username"] = validated_data.get("first_name")
        user = CustomUser.objects.create(**validated_data)
        user.set_password(validated_data["password"])

        user.save()
        print(user)

        try:
            user_profile = UserProfile.objects.get(user=user)
            if user_intent is not None:
                user_profile.user_intent = user_intent
            if role is not None:
                user_profile.role = role
            user_profile.save()
        except UserProfile.DoesNotExist:
            print(f"UserProfile not found for user: {user.email}")

        return user


class VerifyEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    verification_code = serializers.CharField(max_length=6)


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    new_password = serializers.CharField()
    confirm_new_password = serializers.CharField()


class ContactUsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    message = serializers.CharField()
    agreed_to_policy = serializers.BooleanField()

    def validate_agreed_to_policy(self, value):
        if not value:
            raise serializers.ValidationError(
                "You must agree to the privacy policy to submit this form."
            )
        return value


class UpdateProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(
        required=False
    )  # Explicitly define as ImageField, optional

    class Meta:
        model = UserProfile  # Target UserProfile model
        fields = ["profile_picture", "gender"]


class UserProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(source="user.first_name")
    last_name = serializers.CharField(source="user.last_name")
    email = serializers.EmailField(source="user.email")

    class Meta:
        model = UserProfile
        exclude = ["user"]
        # fields = "__all__"
        # read_only_fields=["user"]

    def create(self, validated_data):
        print(validated_data)
        user_data = validated_data.pop("user", {})

        user = self.context["request"].user  # Or create a new user here if needed
        for attr, val in user_data.items():
            setattr(user, attr, val)
            user.save()

        profile = UserProfile.objects.create(user=user, **validated_data)
        return profile

    def update(self, instance, validated_data):
        print(validated_data)
        user_data = validated_data.pop("user", {})

        # Update the related User model
        user = instance.user

        for attr, val in user_data.items():
            setattr(user, attr, val)

        user.save()

        # Update the UserProfile model
        return super().update(instance, validated_data)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_new_password = serializers.CharField(write_only=True)

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate(self, attrs):
        new_password = attrs.get("new_password")
        confirm_new_password = attrs.get("confirm_new_password")

        # Check if the new password matches the confirmation
        if new_password != confirm_new_password:
            raise serializers.ValidationError(
                {"confirm_new_password": "New passwords do not match."}
            )

        # Perform additional validation on the new password if needed
        if len(new_password) < 8:
            raise serializers.ValidationError(
                {"new_password": "New password must be at least 8 characters long."}
            )

        return attrs

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()


class UserAssignmentSerializer(serializers.ModelSerializer):
    admin_email = serializers.EmailField(source="admin.email", read_only=True)
    user_email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = UserAssignment
        fields = ["id", "admin_email", "user_email", "assigned_at"]
