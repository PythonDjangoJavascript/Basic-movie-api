from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializes Default User model provided by django"""

    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', ]
        extra_kwargs = {
            'password': {'write_only': True, }
        }

    def save(self, **kwargs):
        """Overriding Save method to verify password2 and apply setPass method
        to hash Password"""

        pass1 = self.validated_data['password']
        pass2 = self.validated_data['password2']
        email = self.validated_data['email']
        username = self.validated_data['username']

        if pass1 != pass2:
            raise serializers.ValidationError("Password did not match!")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This email already been used')
        # user going to validated by django by default
        account = User(email=email, username=username)
        account.set_password(pass1)  # set hasshed password
        account.save()

        return account
