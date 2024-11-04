from rest_framework import serializers

from users.models import CustomUser


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_blocked','join_date','is_superuser']
